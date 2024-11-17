"""python -m organic_company_history.basis"""
import polars as pl
import pandera as pa
from pandera.typing import DataFrame
from pandera.polars import DataFrameModel

from .polars_llm import PolarsLLM

NUM_EMPLOYEES = 5
MIN_UNIQUE_PAYCODES = 10
FTE_HOURS_PER_WEEK = 35


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
    pay_code: pa.String
    hours: float = pa.Field(nullable=True)
    amount: float = pa.Field(nullable=True)

    class Config:
        coerce = True


class PayrollDefinitions(DataFrameModel):
    pay_code: pa.String
    pay_code_description: pa.String
    pay_category: pa.String

    class Config:
        coerce = True


def format_paycode_data_as_listing(df: DataFrame[PayrollDefinitions]) -> str:
    """Formats the paycode data as a string to be used as part of an LLM query."""
    return str().join("\n    - " + df["pay_code"] + ": " + df["pay_code_description"])


hr_expert = PolarsLLM(
    name="ac-knitting-hr",
    expertise="Knitting and HR data",
    schema=HR,
    reply_parser=lambda df: df.with_columns(pl.col("hire_date").str.to_date()),
    questioner=f"Generate data for {NUM_EMPLOYEES} employees for a knitting company",
)

paycode_definitions_expert = PolarsLLM(
    name="ac-knitting-paycode",
    expertise="Payroll Systems and Administration",
    schema=PayrollDefinitions,
    questioner=(
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
    reply_parser=lambda df: df.with_columns(
        pl.col("hours").cast(pl.Float64, strict=False),
        pl.col("amount").cast(pl.Float64, strict=False),
    ),
    questioner=lambda contract_type, job_title, weekly_hours, paycode_listing: (
        f"Generate one week's worth of payroll data for a {contract_type} {job_title} "
        f"who works {weekly_hours} hours per week. "
        f"Only use pay_codes from the following list:\n{paycode_listing}"
    ),
)

hr_data = hr_expert.get_dataframe().with_columns(
    pl.col("fte").mul(FTE_HOURS_PER_WEEK).alias("weekly_hours")
)
print(f"\n\nhr_data:\n{hr_data}")

paycode_data = paycode_definitions_expert.get_dataframe()
print(f"\n\npaycode_data:\n{paycode_data}")

payroll_dfs = [
    payroll_expert.get_dataframe(
        contract_type=row["contract_type"],
        job_title=row["job_title"],
        weekly_hours=row["weekly_hours"],
        paycode_listing=format_paycode_data_as_listing(paycode_data),
    ).with_columns(pl.lit(row["employee_code"]).alias("employee_code"))
    for row in hr_data.rows(named=True)
]

payroll_data = pl.concat(payroll_dfs)
print(f"\n\npayroll_data:\n{payroll_data}")
