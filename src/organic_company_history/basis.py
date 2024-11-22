"""python -m organic_company_history.basis"""
import polars as pl
from loguru import logger
from typing import NamedTuple
from functools import lru_cache
import random
import pandera as pa
from pandera.typing import DataFrame
from pandera.polars import DataFrameModel

from .polars_llm import PolarsLLM

NUM_EMPLOYEES = 5
MIN_UNIQUE_PAYCODES = 8
MIN_UNIQUE_TIMECODES = 6
MIN_PRODUCTS = 4
MAX_TIMESHEETS = 6
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
    time_code: pa.String = pa.Field(unique=True)
    time_code_description: pa.String
    time_category: pa.String


class Timesheets(DataFrameModel):
    weekday: pa.String = pa.Field(
        isin=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
    )
    time_code: pa.String
    hours: float


class ProductLine(DataFrameModel):
    product_category: pa.String
    product_name: pa.String
    product_description: pa.String
    price: float
    cost_materials: float


class Experts(NamedTuple):
    hr: PolarsLLM
    payroll_admin: PolarsLLM
    timesheet_admin: PolarsLLM
    timesheet_data_entry: PolarsLLM
    payroll_data_entry: PolarsLLM
    product_expert: PolarsLLM


class GeneratedData(NamedTuple):
    hr: DataFrame[HR]
    payroll_definitions: DataFrame[PayrollDefinitions]
    timesheet_codes: DataFrame[TimesheetCodes]
    timesheets: DataFrame[Timesheets]
    payroll: DataFrame[Payroll]
    products: DataFrame[ProductLine]


def format_code_description_as_listing(
    df: DataFrame, code: str, description: str
) -> str:
    """Formats a 'code' and 'description' fields as a string list to be used as
    part of an LLM query."""
    return str().join("\n    - " + df[code] + ": " + df[description])


def make_data_for_industry(industry: str) -> GeneratedData:
    experts = init_experts(industry)
    data = generate_data(experts)
    return data


@lru_cache()
def get_typical_monthly_salary_for_job_title(job_title: str) -> int:
    """Get the typical monthly salary for a given job title

    Args:
        job_title (string): the job to get the monthly salary for
    """
    return random.randrange(start=2000, stop=30000)


@lru_cache
def get_number_of_hours_worked_for_day(
    weekday: str, job_title: str, time_code: str
) -> int:
    """Get the number of hours that `job_title` worked for a given `weekday`

    Args:
        weekday (string): the day of the week to get hours worked
        job_title (string): the job title to get hours worked
        time_code (string): the time code that hours were logged against
    """
    return random.randrange(start=0, stop=16)


def init_experts(industry: str) -> Experts:
    name_prefix = f"user/{industry.replace(' ','-')}"
    return Experts(
        hr=PolarsLLM(
            name=f"{name_prefix}/hr",
            expertise=f"{industry.title()} and HR data",
            schema=HR,
            reply_parser=lambda df: df.with_columns(pl.col("hire_date").str.to_date()),
            questioner=f"Generate data for {NUM_EMPLOYEES} employees for a {industry} company",
        ),
        payroll_admin=PolarsLLM(
            name=f"{name_prefix}/payroll-admin",
            expertise=f"Payroll Systems for {industry.title()}",
            schema=PayrollDefinitions,
            reply_parser=lambda df: df.with_columns(
                pl.col("pay_code").str.to_uppercase()
            ),
            questioner=(
                "Generate a paycode mapping file that we can use to set up a "
                f"payroll system for a {industry} company. This should include all paycodes "
                "we would expect to pay to our employees. Include codes for ordinary, "
                "overtime, and holiday rates. Different leave types should use different pay codes. "
                f"There should be at least {MIN_UNIQUE_PAYCODES} different paycodes."
            ),
        ),
        timesheet_admin=PolarsLLM(
            name=f"{name_prefix}/timesheet-admin",
            expertise=f"{industry.title()} and configuring Timesheeting systems",
            schema=TimesheetCodes,
            reply_parser=lambda df: df.with_columns(
                pl.col("time_code").cast(pl.String)
            ),
            questioner=lambda job_titles: (
                f"Generate a CSV a {industry} company can use to configure a "
                f"timesheet system. The current list of job titles is: {', '.join(job_titles)}. "
                f"There should be at least {MIN_UNIQUE_TIMECODES} different time codes. "
                "time_code should be short and unique."
            ),
        ),
        timesheet_data_entry=PolarsLLM(
            name=f"{name_prefix}/timesheet-peon",
            expertise=f"Filling in timesheets for employees in a {industry} company.",
            schema=Timesheets,
            reply_parser=lambda df: df.with_columns(
                pl.col("time_code").cast(pl.String)
            ),
            questioner=lambda job_title, time_code_csv, weekly_hours: (
                f"Fill in 3 days of timesheets for a {job_title} who works roughly "
                f"{weekly_hours} per week. "
                f"Only use time_codes from the following dataset: \n{time_code_csv}\n"
                "If an employee works multiple time codes in one day, they should be on "
                "separate rows. "
                f"Do not produce more than {MAX_TIMESHEETS} rows."
            ),
            tools=[get_number_of_hours_worked_for_day],
        ),
        payroll_data_entry=PolarsLLM(
            name=f"{name_prefix}/payroll-peon",
            expertise=f"Payroll and {industry.title()}",
            schema=Payroll,
            reply_parser=lambda df: df.with_columns(
                pl.col("pay_code").str.to_uppercase(),
                pl.col("hours").cast(pl.Float64, strict=False),
                pl.col("amount").cast(pl.Float64, strict=False),
            ),
            questioner=lambda contract_type, job_title, weekly_hours, paycode_csv: (
                f"Generate one week's worth of payroll data for a {contract_type} {job_title} "
                f"who works {weekly_hours} hours per week. "
                f"Only use pay_codes from the following dataset:\n{paycode_csv}\n"
                "Avoid having multiple rows with the same 'pay_code' or 'amount' values"
            ),
            tools=[get_typical_monthly_salary_for_job_title],
        ),
        product_expert=PolarsLLM(
            name=f"{name_prefix}/product",
            expertise=f"E-Commerce, {industry.title()}, eBay",
            schema=ProductLine,
            questioner=(
                f"Generate a variety of products our {industry} company can sell on our "
                "website and eBay store. It should have a good mix of different items, styles "
                " and themes. The 'product_description' field should be kept to one sentence. "
                "Each product_category should have more than one product. "
                f"Generate at least {MIN_PRODUCTS} different products."
            ),
        ),
    )


def generate_data(experts: Experts) -> GeneratedData:
    logger.info("generating hr...")
    hr = experts.hr.generate_data().with_columns(
        pl.col("fte").mul(FTE_HOURS_PER_WEEK).alias("weekly_hours")
    )

    logger.info("generating timesheet_codes...")
    timesheet_codes = experts.timesheet_admin.generate_data(job_titles=hr["job_title"])

    logger.info("generating timesheets...")
    timesheet_dfs = [
        (
            experts.timesheet_data_entry.generate_data(
                start_new_conversation=True,
                job_title=row["job_title"],
                weekly_hours=row["weekly_hours"],
                time_code_csv=timesheet_codes[
                    ["time_code", "time_code_description"]
                ].write_csv(),
            ).with_columns(pl.lit(row["employee_code"]).alias("employee_code"))
        )
        for row in hr.rows(named=True)
    ]
    timesheets = pl.concat(timesheet_dfs)
    logger.info(timesheets)

    logger.info("generating payroll_definitions...")
    payroll_definitions = experts.payroll_admin.generate_data()

    logger.info("generating payroll...")
    payroll_dfs = [
        (
            experts.payroll_data_entry.generate_data(
                start_new_conversation=True,
                contract_type=row["contract_type"],
                job_title=row["job_title"],
                weekly_hours=row["weekly_hours"],
                paycode_csv=payroll_definitions[
                    ["pay_code", "pay_code_description"]
                ].write_csv(),
            ).with_columns(
                pl.lit(row["employee_code"]).alias("employee_code"),
            )
        )
        for row in hr.rows(named=True)
    ]
    payroll = pl.concat(payroll_dfs)
    logger.info(payroll)

    logger.info("generating products...")
    products = experts.product_expert.generate_data()

    return GeneratedData(
        hr=hr,
        payroll_definitions=payroll_definitions,
        timesheet_codes=timesheet_codes,
        timesheets=timesheets,
        payroll=payroll,
        products=products,
    )
