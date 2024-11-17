from typing import Type, Callable, Any, Sequence
import ollama
from ollama._types import Message, Tool, ToolCall
from collections.abc import Mapping
import string
import polars as pl
from typing import NamedTuple
from io import BytesIO
import pandera as pa
from pandera.typing import DataFrame, Series
from pandera.polars import DataFrameModel
import polars.selectors as cs


DEFAULT_BASE_MODEL = "llama3.1"

DEFAULT_MAX_CORRECTIONS = 3
"""Number of attempts to correct the generated CSV using feedback"""

DEFAULT_MAX_RETRIES = 3
"""Number of complete retries"""


SYSTEM_MESSAGE_CSV_REQS = (
    "Provide responses as 'csv' format only. "
    "Don't include any text that is not part of the CSV. "
    "All dates should be in YYYY-MM-DD format. "
    "Ensure all fields have values. There should be no consecutive commas. "
    "Ensure all values are able to be coerced into that field's data type. "
    "Boolean fields should use the values true and false. "
)


class ColumnCheck(NamedTuple):
    correct: set[str]
    missing: set[str]
    extra: set[str]

class CSVFormatError(Exception): 
    """Raised when the LLM has generated an invalid CSV"""
    column_check: ColumnCheck

    def __init__(self, *args, column_check: ColumnCheck, **kwargs) -> None:
        self.column_check = column_check
        super().__init__(*args, **kwargs)



class PolarsLLM:
    name: str
    base_model: str
    expertise: str
    schema: Type[DataFrameModel]
    reply_parser: Callable[[pl.DataFrame], pl.DataFrame]
    questioner: Callable[..., str]
    tools: dict[str, Callable]
    formatted_tools: Sequence[Tool]

    message_history: list[Message]

    modelfile: str

    def __init__(
        self,
        name: str,
        expertise: str,
        schema: Type[DataFrameModel],
        questioner: str | Callable[..., str],
        reply_parser: Callable[[pl.DataFrame], pl.DataFrame] | None = None,
        base_model: str = DEFAULT_BASE_MODEL,
        tools: list[Callable] = list()
    ):
        self.name = name
        self.schema = schema
        self.expertise = expertise
        self.base_model = base_model
        self.message_history = list()
        self.tools = {tool.__name__: tool for tool in tools}
        self.formatted_tools = self.format_tools()

        if reply_parser is None:
            self.reply_parser = lambda df: df
        else:
            self.reply_parser = reply_parser

        if isinstance(questioner, str):
            self.questioner = lambda: questioner
        else:
            self.questioner = questioner

        self.modelfile = self.make_modelfile()

        ollama.create(model=name, modelfile=self.modelfile)
        print(f"created model {name} using {base_model}")  # TODO: convert to logs

    def __repr__(self) -> str:
        return f"<PolarsLLM(name={self.name})>"

    def make_modelfile(self):
        system_msg = (
            f"You are an expert in {self.expertise}. "
            f"{SYSTEM_MESSAGE_CSV_REQS}"
            f"The fields and data types required are: {format_pandera_model_as_instruction(self.schema)}"
        )

        return format_modelfile(base_model=self.base_model, system_msg=system_msg)

    def get_dataframe(self, **kwargs) -> pl.DataFrame:
        return self.generate_data(**kwargs)

    def parse_reply(self, reply: pl.DataFrame) -> pl.DataFrame:
        return self.reply_parser(reply).select(self.schema_cols).pipe(self.schema)

    def send_chat_message(self, message:str) -> Mapping[str, Any]:
        formatted_message = self.format_user_message(message)
        self.message_history.append(formatted_message)

        response = ollama.chat(
            model=self.name,
            messages=self.message_history + [formatted_message],
            tools=self.formatted_tools
        )

        self.message_history.append(response)
        return response

    def format_tools(self) -> Sequence[Tool]:
        return [format_tool(tool) for tool in self.tools.values()]

    def format_user_message(self, message: str) -> Message:
        return {"role": "user", "content": message}


    def generate_data(self, **kwargs) -> pl.DataFrame:
        self.message_history = []
        errors = []
        question = self.questioner(**kwargs)
        while len(errors) <= DEFAULT_MAX_RETRIES:
            num_corrections = 0
            while num_corrections <= DEFAULT_MAX_CORRECTIONS:
                response = self.send_chat_message(question)

                if response["message"].get("tool_calls"):
                    response = self.use_tools(response["message"]["tool_calls"])

                response_message = response["message"]
                reply = format_first_line_of_csv(response_message["content"])

                column_check = self.check_reply_columns(reply)

                if not column_check.correct:
                    question = (
                        "That didn't include any valid column names in the first row. "
                        f"Expected: {self.schema_cols}"
                    )
                    num_corrections += 1
                    continue

                if column_check.missing:
                    question = (
                        f"The following column names were not found in the first row: {column_check.missing}. "
                    )

                    if column_check.extra:
                        question += f"Additionally the following column names were not recognized: {column_check.extra}"

                    num_corrections += 1
                    continue

                try:
                    return self.parse_reply(polars_from_csv_string(reply))
                except Exception as e:
                    # TODO: feedback errors into LLM and ask to regenerate
                    errors.append(e)
                    continue

        raise Exception(
            f"Could not generate data after {len(errors)} attempts!:\n{'\n'.join(errors)}"
        )

    def use_tools(self, calls=list[dict]) -> Message:
        for call in calls:
            try:
                func = self.tools[call["function"]["name"]]
            except KeyError:
                continue

            kwargs = call["function"]["arguments"]

            answer = str(func(**kwargs))

            formatted_kwargs = ", ".join([f"{kwarg}={repr(value)}" for kwarg, value in kwargs.items()])
            print(f"used tool: {func.__name__}({formatted_kwargs}): {answer}")

            self.message_history.append({
                "role": "tool",
                "content": answer,
            })

        response = ollama.chat(
            model=self.name,
            messages=self.message_history,
        )

        self.message_history.append(response)

        return response


    @property
    def schema_cols(self) -> set[str]:
        return set(self.schema.to_schema().columns.keys())

    def check_reply_columns(self, reply: str) -> ColumnCheck:
        reply_cols: set[str] = set(reply.lower().split("\n")[0].split(","))
        expected_cols = self.schema_cols

        return ColumnCheck(
            correct = expected_cols & reply_cols,
            missing = expected_cols - reply_cols,
            extra = reply_cols - expected_cols
        )


def format_modelfile(base_model: str, system_msg: str) -> str:
    return f"FROM {base_model}\nSYSTEM {system_msg}\n"


def polars_from_csv_string(csv_string: str) -> pl.DataFrame:
    bytes_data = BytesIO(bytes(csv_string.strip(), "utf-8"))

    raw_df = pl.read_csv(bytes_data)

    return raw_df.with_columns(
        cs.string().map_batches(lambda s: s.str.strip_chars(" '\""))
    )


def format_pandera_model_as_instruction(model: Type[DataFrameModel]) -> str:
    dtypes = model.to_schema().dtypes
    result = "; ".join(
        [
            f"{col_name}={type(dtype).__name__.rstrip(string.digits).lower()}"
            for col_name, dtype in dtypes.items()
        ]
    )

    return result

def format_first_line_of_csv(csv_string: str) -> str:
    """Formats the first line to be lower_case_with_underscores - fixes some easy mistakes"""
    first_line, newline, rest = csv_string.partition("\n")
    return first_line.lower().strip().replace(" ", "_").replace('"', "") + newline + rest

def format_tool(func: Callable) -> Tool:

    properties = format_tool_properties(func)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip().partition("\n")[0],
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": list(properties.keys())
            }
        }
    }


def format_tool_properties(func: Callable) -> dict:
    """Formats the properties dict of a tool - assumes the docstring is google formatted

    TODO : this kinda sucks?
    """

    doc = func.__doc__
    kwargs = [kwarg for kwarg in func.__annotations__ if kwarg != "return"]

    if not doc or "Args:" not in doc:
        raise ValueError(
            f"Could not find 'Args' in the docstring for {func.__name__} "
            "when attempting to format tool properties. Please adjust docstring!"
        )

    arg_lines = doc.partition("Args:")[2].strip().split("\n")
    tool_properties = {}
    for arg_line in arg_lines:
        name_and_type, _, description = (x.strip() for x in arg_line.partition(":"))
        name, _, typ = (x.strip().strip("()") for x in name_and_type.partition(" "))

        if name not in kwargs:
            continue

        tool_properties[name] = {"type": typ, "description": description}

    if len(tool_properties) != len(kwargs):
        missing_kwargs = [kw for kw in kwargs if kw not in tool_properties]
        raise ValueError(
            f"Could not find details for the following kwargs: {missing_kwargs} "
            f"in the docstring for {func.__name__} Please adjust docstring."
        )

    return tool_properties

