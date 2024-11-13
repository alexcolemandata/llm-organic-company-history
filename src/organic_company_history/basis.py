"""python -m organic_company_history.basis"""
import polars as pl
import pandera as pa
from pandera.polars import DataFrameModel

from .polars_llm import PolarsLLM

NUM_EMPLOYEES = 5
MIN_UNIQUE_PAYCODES = 18


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


class PayrollDefinitions(DataFrameModel):
    pay_code: pa.String
    pay_code_description: pa.String
    pay_category: pa.String

    class Config:
        coerce = True


hr_expert = PolarsLLM(
    name="ac-knitting-hr",
    expertise="Knitting and HR data",
    schema=HR,
    response_parser=lambda df: df.with_columns(pl.col("hire_date").str.to_date()),
    message=f"Generate data for {NUM_EMPLOYEES} employees for a knitting company",
)

paycode_definitions_expert = PolarsLLM(
    name="ac-knitting-paycode",
    expertise="Payroll Systems and Administration",
    schema=PayrollDefinitions,
    message=(
        "Generate a paycode mapping file that we can use to set up a "
        "payroll system for a knitting company. This should include all paycodes "
        "we would expect to pay to our employees. Different leave types should use "
        f"different paycodes. There should be at least {MIN_UNIQUE_PAYCODES} different paycodes."
    ),
)

payroll_expert = PolarsLLM(
    name="ac-knitting-payroll",
    expertise="Payroll and Knitting",
    schema=Payroll,
    response_parser=lambda df: df.with_columns(
        pl.col("payroll_run_date").str.to_datetime()
    ),
    message=lambda employee_code, contract_type, job_title: (
        f"Generate one week's worth of payroll data for the following employee: "
        f"{employee_code=}, {contract_type=}, {job_title=}"
    ),
)

hr_data = hr_expert.get_dataframe()
print(f"\n\nhr_data:\n{hr_data}")

paycode_data = paycode_definitions_expert.get_dataframe()
print(f"\n\npaycode_data:\n{paycode_data}")

payroll_data = pl.concat(
    payroll_expert.get_dataframe(
        employee_code=row["employee_code"],
        contract_type=row["contract_type"],
        job_title=row["job_title"],
    )
    for row in hr_data.rows(named=True)
)
print(f"\n\npayroll_data:\n{payroll_data}")
