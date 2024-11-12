"""python -m organic_company_history.basis"""
import polars as pl
import pandera as pa
from pandera.polars import DataFrameModel

from .polars_llm import PolarsLLM

NUM_EMPLOYEES = 5


class HR(DataFrameModel):
    employee_code: pa.String
    name: pa.String
    hire_date: pa.Timestamp
    contract_type: pa.String
    fte: float
    department: pa.String
    job_title: pa.String

    class Config:
        coerce = True


class Payroll(DataFrameModel):
    employee_code: pa.String
    pay_code: pa.String
    pay_code_description: pa.String
    hours: float
    amount: float
    payroll_run_date: pa.Timestamp

    class Config:
        coerce = True


class HRExpert(PolarsLLM):
    def make_message_content(self) -> str:
        return f"Generate data for {NUM_EMPLOYEES} employees for a knitting company"

    def parse_response(self, response: pl.DataFrame) -> pl.DataFrame:
        result = response.with_columns(pl.col("hire_date").str.to_date())

        return result.pipe(self.schema, lazy=True)


class PayrollExpert(PolarsLLM):
    def make_message_content(
        self, employee_code: str, contract_type: str, job_title: str
    ) -> str:
        return (
            f"Generate one week's worth of payroll data for the following employee: "
            f"{employee_code=}, {contract_type=}, {job_title=}"
        )

    def parse_response(self, response: pl.DataFrame) -> pl.DataFrame:
        result = response.with_columns(pl.col("payroll_run_date").str.to_datetime())

        return result.pipe(self.schema, lazy=True)


hr_expert = HRExpert(name="ac-knitting-hr", expertise="Knitting and HR data", schema=HR)


payroll_expert = PayrollExpert(
    name="ac-knitting-payroll", expertise="Payroll and Knitting", schema=Payroll
)

hr_data = hr_expert.get_dataframe()

print(f"\n\nhr_data:\n{hr_data}")

payroll_data = pl.concat(
    payroll_expert.get_dataframe(
        employee_code=row["employee_code"],
        contract_type=row["contract_type"],
        job_title=row["job_title"],
    )
    for row in hr_data.rows(named=True)
)

print(f"\n\npayroll_data:\n{payroll_data}")
