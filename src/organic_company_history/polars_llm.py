from typing import Type, Callable, Any
import ollama
from ollama._types import Message
from collections.abc import Mapping
import string
import polars as pl
from typing import NamedTuple
from io import BytesIO
import pandera as pa
from pandera.typing import DataFrame, Series
from pandera.polars import DataFrameModel
import polars.selectors as cs



DEFAULT_MAX_CORRECTIONS = 3
"""Number of attempts to correct the generated CSV using feedback"""

DEFAULT_MAX_RETRIES = 3
"""Number of complete retries"""

DEFAULT_BASE_MODEL = "llama3.1"

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
    ):
        self.name = name
        self.schema = schema
        self.expertise = expertise
        self.base_model = base_model
        self.message_history = list()

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
        return ollama.chat(
            model=self.name,
            messages=self.message_history + [formatted_message]
        )

    def format_user_message(self, message: str) -> Message:
        return {"role": "user", "content": message}


    def generate_data(self, **kwargs) -> pl.DataFrame:
        errors = []
        question = self.questioner(**kwargs)
        while len(errors) <= DEFAULT_MAX_RETRIES:
            num_corrections = 0
            while num_corrections <= DEFAULT_MAX_CORRECTIONS:
                response = self.send_chat_message(question)
                response_message = response["message"]
                self.message_history.append(response_message)
                reply = response_message["content"]

                column_check = self.check_reply_columns(reply)

                if not column_check.correct:
                    # errors.append(CSVFormatError("No columns correct", column_check=column_check))
                    question = (
                        f"Column names were missing, expected: {self.schema_cols}"
                    )
                    num_corrections += 1
                    continue

                if column_check.missing:
                    # errors.append(CSVFormatError("Missing columns", column_check=column_check))
                    breakpoint()
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


    @property
    def schema_cols(self) -> set[str]:
        return set(self.schema.to_schema().columns.keys())

    def check_reply_columns(self, reply: str) -> ColumnCheck:
        reply_cols: set[str] = set(reply.split("\n")[0].replace('"', "").split(","))
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
