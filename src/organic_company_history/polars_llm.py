from typing import Type, Callable, Any, Sequence, Literal
import ollama
from ollama._types import Message, Tool, BaseGenerateResponse
from collections.abc import Mapping
import string
import polars as pl
from typing import NamedTuple
from io import BytesIO
from pandera.polars import DataFrameModel
import polars.selectors as cs
from . import database
from loguru import logger


DEFAULT_BASE_MODEL = "llama3.1"

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


Role = Literal["user", "assistant", "system", "tool"]


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
    """A LLM which (attempts) to return polars dataframes as responses."""

    name: str
    expertise: str
    schema: Type[DataFrameModel]
    reply_parser: Callable[[pl.DataFrame], pl.DataFrame]
    questioner: Callable[..., str]
    formatted_tools: Sequence[Tool]

    modelfile: str

    model: database.Model
    current_conversation: database.Conversation
    callable_tools: dict[str, Callable]

    def __init__(
        self,
        name: str,
        expertise: str,
        schema: Type[DataFrameModel],
        questioner: str | Callable[..., str],
        reply_parser: Callable[[pl.DataFrame], pl.DataFrame] | None = None,
        base_model: str = DEFAULT_BASE_MODEL,
        tools: list[Callable] = list(),
    ) -> None:
        self.name = name
        self.schema = schema
        self.expertise = expertise

        if reply_parser is None:
            self.reply_parser = lambda df: df
        else:
            self.reply_parser = reply_parser

        if isinstance(questioner, str):
            self.questioner = lambda: questioner
        else:
            self.questioner = questioner

        modelfile = self.make_modelfile(base_model=base_model)

        ollama.create(model=name, modelfile=modelfile)
        logger.info(f"created model {name} using {base_model}")  # TODO: convert to logs
        logger.debug(f"{name}.Modelfile\n{modelfile}")

        # janky orm things
        model = database.Model(name=name, base_model=base_model, modelfile=modelfile)

        database.session.add(model)
        database.session.commit()
        self.model = model

        self.init_tools(tools)
        self.formatted_tools = self.format_tools()
        self.start_conversation()

    @property
    def latest_message(self) -> database.Message:
        return self.current_conversation.messages[-1]

    @property
    def message_history(self) -> list[Message]:
        return [
            {"role": message.role, "content": message.content}
            for message in self.current_conversation.messages
        ]

    def init_tools(self, tools: list[Callable]) -> None:
        self.callable_tools = {tool.__name__: tool for tool in tools}
        for tool in tools:
            orm_tool = database.Tool(
                model_id=self.model.id,
                name=tool.__name__,
                docstring=tool.__doc__,
                annotations=str(tool.__annotations__),
                is_hallucination=False,
            )
            database.session.add(orm_tool)
        database.session.commit()

    def start_conversation(self) -> None:
        """Start a new conversation with message history"""
        logger.debug(f"{self} Starting new conversation")
        conversation = database.Conversation(model_id=self.model.id)
        database.session.add(conversation)
        database.session.commit()
        self.current_conversation = conversation

    def record_message(self, msg: Message) -> None:
        if "content" in msg:
            message = database.Message(
                conversation_id=self.current_conversation.id,
                role=msg["role"],
                content=msg["content"] or "",
            )
        else:
            breakpoint()
            return None

        database.session.add(message)
        database.session.commit()
        return None

    def __repr__(self) -> str:
        return f"<PolarsLLM(name={self.name})>"

    def make_modelfile(self, base_model: str):
        system_msg = (
            f"You are an expert in {self.expertise}. "
            f"{SYSTEM_MESSAGE_CSV_REQS}"
            f"The fields and data types required are: {format_pandera_model_as_instruction(self.schema)}"
        )

        return format_modelfile(base_model=base_model, system_msg=system_msg)

    def parse_reply(self, reply: pl.DataFrame) -> pl.DataFrame:
        return self.reply_parser(reply).select(self.schema_cols).pipe(self.schema)

    def get_response(self) -> Mapping[str, Any]:
        response = ollama.chat(
            model=self.name, messages=self.message_history, tools=self.formatted_tools
        )
        self.record_message(response["message"])
        self.record_response(response)  # response holds the metadata of the message

        return response

    def record_response(self, response: Mapping[str, Any]) -> None:
        database.session.add(
            database.Response(
                **{
                    field: value
                    for field, value in response.items()
                    if field
                    in [
                        "done_reason",
                        "eval_count",
                        "eval_duration",
                        "load_duration",
                        "prompt_eval_count",
                        "prompt_eval_duration",
                        "total_duration",
                    ]
                },
                message_id=self.current_conversation.messages[-1].id,
            )
        )
        database.session.commit()
        return None

    def send_message(self, role: Role, message: str) -> Mapping[str, Any]:
        formatted_message = self.format_message(role=role, message=message)
        self.record_message(formatted_message)

        return self.get_response()

    def format_tools(self) -> Sequence[Tool]:
        return [format_tool(tool) for tool in self.callable_tools.values()]

    def format_message(self, role: Role, message: str) -> Message:
        return {"role": role, "content": message}

    def generate_data(
        self, start_new_conversation: bool = False, **kwargs
    ) -> pl.DataFrame:
        if start_new_conversation and (len(self.current_conversation.messages) > 0):
            self.start_conversation()

        question = self.questioner(**kwargs)
        num_retries = -1
        reply = ""
        while num_retries <= DEFAULT_MAX_RETRIES:
            num_retries += 1

            if num_retries > 1:
                logger.warning(
                    f"{num_retries=}\n\nreply:\n{reply}\n\nfollow up question: {question}"
                )
            else:
                logger.info(f"question: {question}")

            response = self.send_message("user", question)

            if response["message"].get("tool_calls"):
                response = self.use_tools(response["message"]["tool_calls"])

            response_message = response["message"]
            reply = format_first_line_of_csv(response_message["content"])

            column_check = self.check_reply_columns(reply)

            if not column_check.correct:
                question = (
                    "The first row did not look correct. "
                    f"It should only have the column names: {self.schema_cols}"
                )
                continue

            if column_check.missing:
                question = f"That was incorrect. The first row was missing these columns: {column_check.missing}. "

                if column_check.extra:
                    # this might confuse it, telling the model only the wrong
                    # columns seems to be more reliable?
                    # question += f"Additionally the following column names were not recognized: {column_check.extra}"
                    pass

                continue

            try:
                return self.parse_reply(polars_from_csv_string(reply))
            except Exception as e:
                question = str(e)
                continue

        raise Exception(f"Could not generate data for {self.model.name}")

    def get_tool(self, name: str) -> database.Tool:
        tool = database.session.query(database.Tool).filter_by(name=name).first()

        if not tool:
            # llm hallucinated for the first time, create it
            tool = database.Tool(
                model_id=self.model.id, name=name, is_hallucination=True
            )
            database.session.add(tool)
            database.session.commit()

        return tool

    def record_hallucinated_tool_call(
        self, tool: database.Tool, call_args: dict
    ) -> None:
        breakpoint()

        return None

    def use_tool(self, name: str, call_args: dict) -> None:
        tool = self.get_tool(name)

        tool_call = database.ToolCall(
            tool_id=tool.id,
            arguments=call_args,
            message_id=self.latest_message.id,
        )
        database.session.add(tool_call)
        database.session.commit()

        # special case if hallucinated
        if tool.is_hallucination:
            tool_result = database.ToolResult(
                call_id=tool_call.id, was_error=True, value_or_error="Hallucination"
            )

            database.session.add(tool_result)
            database.session.commit()
            return None

        # attempt to run tool
        try:
            result = self.callable_tools[name](**call_args)
        except Exception as e:
            tool_result = database.ToolResult(
                call_id=tool_call.id, was_error=True, value_or_error=str(e)
            )
        else:
            tool_result = database.ToolResult(
                call_id=tool_call.id, was_error=False, value_or_error=str(result)
            )

        database.session.add(tool_result)
        database.session.commit()
        return None

    def use_tools(self, calls=list[dict]) -> Message:
        for call in calls:
            self.use_tool(
                name=call["function"]["name"], call_args=call["function"]["arguments"]
            )

        response = self.send_tool_results()

        return response

    def send_tool_results(self) -> Mapping[str, Any]:
        calls = database.session.query(database.ToolCall).filter_by(
            message_id=self.latest_message.id
        )

        formatted_responses = []
        for call in calls:
            name = call.tool.name
            formatted_args = ", ".join(
                f"{k}={repr(v)}" for k, v in call.arguments.items()
            )
            formatted_responses.append(
                f"{name}({formatted_args}) = {call.result.value_or_error}"
            )

        return self.send_message(role="tool", message="\n".join(formatted_responses))

    @property
    def schema_cols(self) -> set[str]:
        return set(self.schema.to_schema().columns.keys())

    def check_reply_columns(self, reply: str) -> ColumnCheck:
        reply_cols: set[str] = set(reply.lower().split("\n")[0].split(","))
        expected_cols = self.schema_cols

        return ColumnCheck(
            correct=expected_cols & reply_cols,
            missing=expected_cols - reply_cols,
            extra=reply_cols - expected_cols,
        )


def format_modelfile(base_model: str, system_msg: str) -> str:
    return f"FROM {base_model}\nSYSTEM {system_msg}\n"


def polars_from_csv_string(csv_string: str) -> pl.DataFrame:
    bytes_data = BytesIO(bytes(csv_string.partition("\n\n")[0].strip(), "utf-8"))

    raw_df = pl.read_csv(bytes_data, ignore_errors=True, truncate_ragged_lines=True)

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
    return (
        first_line.lower()
        .strip()
        .removeprefix("<|python_tag|>")
        .replace(" ", "_")
        .replace('"', "")
        + newline
        + rest
    )


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
                "required": list(properties.keys()),
            },
        },
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
