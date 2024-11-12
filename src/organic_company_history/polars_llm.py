from typing import Type
import ollama
import string
import polars as pl
from io import BytesIO
import pandera as pa
from pandera.typing import DataFrame, Series
import polars.selectors as cs


DEFAULT_MAX_ATTEMPTS = 3
DEFAULT_BASE_MODEL = "llama3.1"

SYSTEM_MESSAGE_CSV_REQS = (
    "Provide responses as 'csv' format only. "
    "Don't include any text that is not part of the CSV. "
    "All dates should be in YYYY-MM-DD format. "
    "Ensure all fields have values. "
)


class PolarsLLM:
    name: str
    base_model: str
    expertise: str
    schema: Type[pa.DataFrameModel]

    modelfile: str

    def __init__(
        self,
        name: str,
        expertise: str,
        schema: Type[pa.DataFrameModel],
        base_model: str = DEFAULT_BASE_MODEL,
    ):
        self.name = name
        self.schema = schema
        self.expertise = expertise
        self.base_model = base_model
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

    def make_message_content(self, **kwargs) -> str:
        raise NotImplementedError("This method needs to be defined per subclass")

    def get_dataframe(self, **kwargs) -> pl.DataFrame:
        return self.generate_data(**kwargs)

    def parse_response(self, response: pl.DataFrame) -> pl.DataFrame:
        raise NotImplementedError("This method needs to be defined per subclass")

    def generate_data(self, **kwargs) -> pl.DataFrame:
        errors = []
        while len(errors) <= DEFAULT_MAX_ATTEMPTS:
            response = ollama.chat(
                model=self.name,
                messages=[
                    {"role": "user", "content": self.make_message_content(**kwargs)}
                ],
            )["message"]["content"]

            missing, extra = self.get_missing_and_extra_cols_in_response(response)

            if missing:
                # TODO: feedback to LLM and ask to regenerate
                errors.append(ValueError(f"Missing the following columns: {missing}!"))
                pass

            try:
                return self.parse_response(polars_from_csv_string(response))
            except Exception as e:
                # TODO: feedback errors into LLM and ask to regenerate
                errors.append(e)
                pass

        raise Exception(
            f"Could not generate data after {len(errors)} attempts!:\n{errors}"
        )

    def get_missing_and_extra_cols_in_response(
        self, response: str
    ) -> tuple[set[str], set[str]]:
        response_cols: set[str] = set(
            response.split("\n")[0].replace('"', "").split(",")
        )
        expected_cols: set[str] = set(self.schema.to_schema().columns.keys())

        missing = expected_cols - response_cols
        extra = response_cols - expected_cols

        return missing, extra


def format_modelfile(base_model: str, system_msg: str) -> str:
    return f"FROM {base_model}\nSYSTEM {system_msg}\n"


def polars_from_csv_string(csv_string: str) -> pl.DataFrame:
    bytes_data = BytesIO(bytes(csv_string.strip(), "utf-8"))

    raw_df = pl.read_csv(bytes_data)

    return raw_df.with_columns(
        cs.string().map_batches(lambda s: s.str.strip_chars(" '\""))
    )


def format_pandera_model_as_instruction(model: Type[pa.DataFrameModel]) -> str:
    dtypes = model.to_schema().dtypes
    result = "; ".join(
        [
            f"{col_name}={type(dtype).__name__.rstrip(string.digits).lower()}"
            for col_name, dtype in dtypes.items()
        ]
    )

    return result
