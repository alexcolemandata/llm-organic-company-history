"""python -m organic_company_history.basis"""
import polars as pl
import pandera as pa
from pandera.polars import DataFrameModel

from .polars_llm import PolarsLLM

NUM_EMPLOYEES = 10


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
    def make_message_content(self) -> str:
        return (
            f"Generate one month's worth of payroll data for {NUM_EMPLOYEES} "
            "different employees"
        )

    def parse_response(self, response: pl.DataFrame) -> pl.DataFrame:
        breakpoint()
        result = response.with_columns(pl.col("payroll_run_date").str.to_date())

        return result.pipe(self.schema, lazy=True)


hr_expert = HRExpert(name="ac-knitting-hr", expertise="Knitting and HR data", schema=HR)


payroll_expert = PayrollExpert(
    name="ac-knitting-payroll", expertise="Payroll and Knitting", schema=Payroll
)

hr_data = hr_expert.get_dataframe()
payroll_data = payroll_expert.get_dataframe()

print(f"\n\nhr_data:\n{hr_data}")
print(f"\n\npayroll_data:\n{payroll_data}")
