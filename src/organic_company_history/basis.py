"""python -m organic_company_history.basis"""
import polars as pl
import pandera as pa
from pandera.typing import DataFrame
from pandera.polars import DataFrameModel

from .polars_llm import PolarsLLM

NUM_EMPLOYEES = 5
MIN_UNIQUE_PAYCODES = 10
MIN_UNIQUE_TIMECODES = 8
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
    amount: float

    class Config:
        coerce = True


class PayrollDefinitions(DataFrameModel):
    pay_code: pa.String
    pay_code_description: pa.String
    pay_category: pa.String

    class Config:
        coerce = True


class TimesheetCodes(DataFrameModel):
    time_code: pa.String
    time_code_description: pa.String
    time_category: pa.String


class Timesheets(DataFrameModel):
    weekday: pa.String
    time_code: pa.String
    hours: float


def format_code_description_as_listing(
    df: DataFrame, code: str, description: str
) -> str:
    """Formats a 'code' and 'description' fields as a string list to be used as
    part of an LLM query."""
    return str().join("\n    - " + df[code] + ": " + df[description])


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
    reply_parser=lambda df: df.with_columns(pl.col("pay_code").str.to_uppercase()),
    questioner=(
        "Generate a paycode mapping file that we can use to set up a "
        "payroll system for a knitting company. This should include all paycodes "
        "we would expect to pay to our employees. Include codes for ordinary, "
        "overtime, and holiday rates. Different leave types should use "
        f"different paycodes. There should be at least {MIN_UNIQUE_PAYCODES} different paycodes."
    ),
)

timesheet_admin = PolarsLLM(
    name="ac-timesheet-admin",
    expertise="Knitting and configuring Timesheeting systems",
    schema=TimesheetCodes,
    reply_parser=lambda df: df.with_columns(pl.col("time_code").str.to_uppercase()),
    questioner=lambda job_titles: (
        "Generate a CSV we can use to configure our timesheeting system so that "
        "employees can log their time for all their activities. We are a knitting "
        f"company. The list of job titles currently active is: {job_titles}. There "
        f"should be at least {MIN_UNIQUE_TIMECODES} different time codes."
    ),
)

timesheeter = PolarsLLM(
    name="ac-timesheet-peon",
    expertise="Filling in timesheets for employees in a Knitting company.",
    schema=Timesheets,
    questioner=lambda job_title, time_codes, weekly_hours: (
        f"Fill in 1 week of timesheets for a {job_title} who works roughly "
        f"{weekly_hours} per week. "
        "The 'weekday' column should use values like 'Monday', 'Tuesday', 'Saturday', etc. "
        f"Only use time_codes from the following list: \n{time_codes}"
        "Employees can use multiple time_codes in one day, these should be split over many rows. "
        "There should be no more than 12 hours total each day."
    ),
)

payroll_expert = PolarsLLM(
    name="ac-knitting-payroll",
    expertise="Payroll and Knitting",
    schema=Payroll,
    reply_parser=lambda df: df.with_columns(
        pl.col("pay_code").str.to_uppercase(),
        pl.col("hours").cast(pl.Float64, strict=False),
        pl.col("amount").cast(pl.Float64, strict=False),
    ),
    questioner=lambda contract_type, job_title, weekly_hours, paycode_listing: (
        f"Generate one week's worth of payroll data for a {contract_type} {job_title} "
        f"who works {weekly_hours} hours per week. "
        f"Only use pay_codes from the following list:\n{paycode_listing}"
    ),
)

print("\n\ngenerating hr_data...")
hr_data = hr_expert.get_dataframe().with_columns(
    pl.col("fte").mul(FTE_HOURS_PER_WEEK).alias("weekly_hours")
)
print(hr_data)

print("\n\ngenerating paycode_data...")
paycode_data = paycode_definitions_expert.get_dataframe()
print(paycode_data)

print("\n\ngenerating timesheet_codes...")
timesheet_codes = timesheet_admin.get_dataframe(
    job_titles=",".join(hr_data["job_title"])
)
print(timesheet_codes)

print("\n\ngenerating timesheets...")

timesheet_dfs = [
    (
        timesheeter.get_dataframe(
            job_title=row["job_title"],
            weekly_hours=row["weekly_hours"],
            time_codes=format_code_description_as_listing(
                timesheet_codes, code="time_code", description="time_code_description"
            ),
        ).with_columns(pl.lit(row["employee_code"]).alias("employee_code"))
    )
    for row in hr_data.rows(named=True)
]
timesheets = pl.concat(timesheet_dfs)
print(timesheets)


print("\n\ngenerating payroll_data...")
payroll_dfs = [
    (
        payroll_expert.get_dataframe(
            contract_type=row["contract_type"],
            job_title=row["job_title"],
            weekly_hours=row["weekly_hours"],
            paycode_listing=format_code_description_as_listing(
                paycode_data, code="pay_code", description="pay_code_description"
            ),
        ).with_columns(
            pl.lit(row["employee_code"]).alias("employee_code"),
        )
    )
    for row in hr_data.rows(named=True)
]
payroll_data = pl.concat(payroll_dfs)
print(payroll_data)
