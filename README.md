:q
# llm-organic-company-history

A learning project to see how llms can work within a python environment.

## Demo: Generating Data for an Occult Detective Agency

The 'main' script accepts the 'industry' as an input argument when run from the
command line.

For example: Generating data for an Occult Detecive Agency:

```
> python -m organic_company_history.main "Occult Detective Agency"
```

```
------------------------------------------------------------------------------------------------------------------------------------------------------
Generating data for Occult Detective Agency:

23:03:13 | INFO     | polars_llm - created model user/Occult-Detective-Agency/hr using llama3.1
23:03:13 | INFO     | polars_llm - created model user/Occult-Detective-Agency/payroll-admin using llama3.1
23:03:13 | INFO     | polars_llm - created model user/Occult-Detective-Agency/timesheet-admin using llama3.1
23:03:13 | INFO     | polars_llm - created model user/Occult-Detective-Agency/timesheet-peon using llama3.1
23:03:13 | INFO     | polars_llm - created model user/Occult-Detective-Agency/payroll-peon using llama3.1
23:03:13 | INFO     | polars_llm - created model user/Occult-Detective-Agency/product using llama3.1
23:03:13 | INFO     | basis - generating hr...
23:03:13 | INFO     | polars_llm - question: Generate data for 5 employees for a Occult Detective Agency company
23:03:19 | INFO     | polars_llm - success after num_retries=0, num_attempts=0! generated: shape: (5, 7)
┌─────────────────────┬───────────────┬─────────────────────────────────┬──────────────────────────────┬──────┬───────────────┬─────────────────────┐
│ name                ┆ employee_code ┆ job_title                       ┆ department                   ┆ fte  ┆ contract_type ┆ hire_date           │
│ ---                 ┆ ---           ┆ ---                             ┆ ---                          ┆ ---  ┆ ---           ┆ ---                 │
│ str                 ┆ str           ┆ str                             ┆ str                          ┆ f64  ┆ str           ┆ datetime[μs]        │
╞═════════════════════╪═══════════════╪═════════════════════════════════╪══════════════════════════════╪══════╪═══════════════╪═════════════════════╡
│ Lola Luxington      ┆ A-001         ┆ Occult Investigator             ┆ Operations                   ┆ 1.0  ┆ Full-time     ┆ 2022-01-15 00:00:00 │
│ Finnley Fizzlewhack ┆ A-002         ┆ Paranormal Researcher           ┆ Research and Development     ┆ 0.5  ┆ Part-time     ┆ 2019-06-20 00:00:00 │
│ Zelda Zingpocket    ┆ A-003         ┆ Ghost Hunter                    ┆ Operations                   ┆ 1.0  ┆ Full-time     ┆ 2020-03-01 00:00:00 │
│ Balthazar McSnazz   ┆ A-004         ┆ Accountant (Supernatural Asset… ┆ Finance                      ┆ 0.75 ┆ Contract      ┆ 2018-09-15 00:00:00 │
│ Penny Pixelwitch    ┆ A-005         ┆ Social Media Manager (Occult)   ┆ Marketing and Communications ┆ 0.25 ┆ Part-time     ┆ 2021-11-01 00:00:00 │
└─────────────────────┴───────────────┴─────────────────────────────────┴──────────────────────────────┴──────┴───────────────┴─────────────────────┘
23:03:19 | INFO     | basis - generating timesheet_codes...
23:03:19 | INFO     | polars_llm - question: Generate a CSV a Occult Detective Agency company can use to configure a timesheet system. The current list of job titles is: Occult Investigator, Paranormal Researcher, Ghost Hunter, Accountant (Supernatural Assets), Social Media Manager (Occult). There should be at least 6 different time codes. time_code should be short and unique.
23:03:25 | INFO     | polars_llm - success after num_retries=0, num_attempts=0! generated: shape: (9, 3)
┌─────────────────────────────────┬─────────────────────────────────┬───────────┐
│ time_category                   ┆ time_code_description           ┆ time_code │
│ ---                             ┆ ---                             ┆ ---       │
│ str                             ┆ str                             ┆ str       │
╞═════════════════════════════════╪═════════════════════════════════╪═══════════╡
│ Occult Investigator             ┆ Investigation Hours             ┆ INVH      │
│ Paranormal Researcher           ┆ Paranormal Research Time        ┆ PRRC      │
│ Ghost Hunter                    ┆ Ghost Hunting Time              ┆ GHTM      │
│ Accountant (Supernatural Asset… ┆ Assets Valuation and Storage V… ┆ AASV      │
│ Social Media Manager (Occult)   ┆ Social Media Management for Oc… ┆ SMMS      │
│ Ghost Hunter                    ┆ Metaphysical Event Time Alloca… ┆ META      │
│ Occult Investigator             ┆ Education and Training Time     ┆ EDUC      │
│ Paranormal Researcher           ┆ Travel Time for Research Narra… ┆ TTRN      │
│ Accountant (Supernatural Asset… ┆ Office Overhead Costs Valuatio… ┆ OOCV      │
└─────────────────────────────────┴─────────────────────────────────┴───────────┘
23:03:25 | INFO     | basis - generating timesheets...
23:03:25 | INFO     | polars_llm - question: Fill in 3 days of timesheets for a Occult Investigator who works roughly 35.0 per week. Only use time_codes from the following dataset:
time_code,time_code_description
INVH,Investigation Hours
PRRC,Paranormal Research Time
GHTM,Ghost Hunting Time
AASV,Assets Valuation and Storage Value
SMMS,Social Media Management for Occult
META,Metaphysical Event Time Allocation
EDUC,Education and Training Time
TTRN,Travel Time for Research Narratives
OOCV,Office Overhead Costs Valuation

If an employee works multiple time codes in one day, they should be on separate rows. Do not produce more than 6 rows.
23:03:39 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=1

reply:
2023-12-04,monday,invh,9.0
2023-12-05,"Tuesday",PRRC,4.0
2023-12-06,"Wednesday",GHTM,2.0
2023-12-07,"Thursday",AASV,14.0
2023-12-08,"Friday",SMMS,14.0
2023-12-09,"Saturday",META,13.0

follow up question: The first row did not look correct. It should only have the column names: hours,weekday,time_code
23:03:45 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=2

reply:
2023-12-04,monday,invh,9.0
2023-12-05,"Tuesday",PRRC,4.0
2023-12-06,"Wednesday",GHTM,2.0
2023-12-07,"Thursday",AASV,14.0
2023-12-08,"Friday",SMMS,6.25
2023-12-09,"Saturday",META,8.75

follow up question: The first row did not look correct. It should only have the column names: hours,weekday,time_code
23:03:50 | INFO     | polars_llm - success after num_retries=2, num_attempts=0! generated: shape: (5, 3)
┌───────┬───────────┬───────────┐
│ hours ┆ weekday   ┆ time_code │
│ ---   ┆ ---       ┆ ---       │
│ f64   ┆ str       ┆ str       │
╞═══════╪═══════════╪═══════════╡
│ 7.92  ┆ Tuesday   ┆ PRRC      │
│ 2.0   ┆ Wednesday ┆ GHTM      │
│ 14.0  ┆ Thursday  ┆ AASV      │
│ 6.25  ┆ Friday    ┆ SMMS      │
│ 8.75  ┆ Saturday  ┆ META      │
└───────┴───────────┴───────────┘
23:03:50 | INFO     | polars_llm - question: Fill in 3 days of timesheets for a Paranormal Researcher who works roughly 17.5 per week. Only use time_codes from the following dataset:
time_code,time_code_description
INVH,Investigation Hours
PRRC,Paranormal Research Time
GHTM,Ghost Hunting Time
AASV,Assets Valuation and Storage Value
SMMS,Social Media Management for Occult
META,Metaphysical Event Time Allocation
EDUC,Education and Training Time
TTRN,Travel Time for Research Narratives
OOCV,Office Overhead Costs Valuation

If an employee works multiple time codes in one day, they should be on separate rows. Do not produce more than 6 rows.
23:04:04 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=1

reply:
weekday,time_code,hours
"2023-12-04","INVH",7.000000
"2023-12-05","GHTM",0.000000
"2023-12-06","PRRC",14.000000
"2023-12-04","META",1.000000
"2023-12-05","AASV",0.000000
"2023-12-06","TTRN",8.000000

follow up question: Column 'weekday' failed validator number 0: <Check isin: isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])> failure case examples: [{'weekday': '2023-12-04'}, {'weekday': '2023-12-05'}, {'weekday': '2023-12-06'}, {'weekday': '2023-12-04'}, {'weekday': '2023-12-05'}]
23:04:10 | INFO     | polars_llm - success after num_retries=1, num_attempts=0! generated: shape: (6, 3)
┌───────┬───────────┬───────────┐
│ hours ┆ weekday   ┆ time_code │
│ ---   ┆ ---       ┆ ---       │
│ f64   ┆ str       ┆ str       │
╞═══════╪═══════════╪═══════════╡
│ 7.0   ┆ Monday    ┆ INVH      │
│ 0.0   ┆ Tuesday   ┆ GHTM      │
│ 14.0  ┆ Wednesday ┆ PRRC      │
│ 1.0   ┆ Monday    ┆ META      │
│ 0.0   ┆ Tuesday   ┆ AASV      │
│ 8.0   ┆ Wednesday ┆ TTRN      │
└───────┴───────────┴───────────┘
23:04:10 | INFO     | polars_llm - question: Fill in 3 days of timesheets for a Ghost Hunter who works roughly 35.0 per week. Only use time_codes from the following dataset:
time_code,time_code_description
INVH,Investigation Hours
PRRC,Paranormal Research Time
GHTM,Ghost Hunting Time
AASV,Assets Valuation and Storage Value
SMMS,Social Media Management for Occult
META,Metaphysical Event Time Allocation
EDUC,Education and Training Time
TTRN,Travel Time for Research Narratives
OOCV,Office Overhead Costs Valuation

If an employee works multiple time codes in one day, they should be on separate rows. Do not produce more than 6 rows.
23:04:18 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=1

reply:
weekday,time_code,hours
"2024-01-01","INVH",11.0
"2024-01-02","PRRC",13.0
"2024-01-03","GHTM",9.0

follow up question: Column 'weekday' failed validator number 0: <Check isin: isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])> failure case examples: [{'weekday': '2024-01-01'}, {'weekday': '2024-01-02'}, {'weekday': '2024-01-03'}]
23:04:25 | INFO     | polars_llm - success after num_retries=1, num_attempts=0! generated: shape: (3, 3)
┌───────┬───────────┬───────────┐
│ hours ┆ weekday   ┆ time_code │
│ ---   ┆ ---       ┆ ---       │
│ f64   ┆ str       ┆ str       │
╞═══════╪═══════════╪═══════════╡
│ 3.0   ┆ Monday    ┆ INVH      │
│ 14.0  ┆ Tuesday   ┆ PRRC      │
│ 12.0  ┆ Wednesday ┆ GHTM      │
└───────┴───────────┴───────────┘
23:04:25 | INFO     | polars_llm - question: Fill in 3 days of timesheets for a Accountant (Supernatural Assets) who works roughly 26.25 per week. Only use time_codes from the following dataset:
time_code,time_code_description
INVH,Investigation Hours
PRRC,Paranormal Research Time
GHTM,Ghost Hunting Time
AASV,Assets Valuation and Storage Value
SMMS,Social Media Management for Occult
META,Metaphysical Event Time Allocation
EDUC,Education and Training Time
TTRN,Travel Time for Research Narratives
OOCV,Office Overhead Costs Valuation

If an employee works multiple time codes in one day, they should be on separate rows. Do not produce more than 6 rows.
23:04:40 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=1

reply:
weekday,time_code
"2023-12-04","INVH"
"2023-12-04","AASV"
"2023-12-05","PRRC"
"2023-12-05","SMMS"
"2023-12-06","GHTM"
"2023-12-06","META"

follow up question: That was incorrect. The first row was missing these columns: hours.
23:04:49 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=2

reply:
weekday,time_code,hours
"2023-12-04","INVH",4.0
"2023-12-04","AASV",6.0
get_number_of_hours_worked_for_day(job_title='Accountant (Supernatural Assets)', time_code='PRRC', weekday='2023-12-05') = 15
get_number_of_hours_worked_for_day(job_title='Accountant (Supernatural Assets)', time_code='SMMS', weekday='2023-12-05') = 8

follow up question: Column 'weekday' failed validator number 0: <Check isin: isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])> failure case examples: [{'weekday': '2023-12-04'}, {'weekday': '2023-12-04'}, {'weekday': "get_number_of_hours_worked_for_day(job_title='Accountant (Supernatural Assets)"}, {'weekday': "get_number_of_hours_worked_for_day(job_title='Accountant (Supernatural Assets)"}]
expected column 'hours' to have type Float64, got String
23:04:56 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=3

reply:
weekday,time_code,hours
"2023-12-04","INVH",4.0
get_number_of_hours_worked_for_day(job_title='Accountant (Supernatural Assets)', time_code='AASV', weekday='2023-12-04') = 6
get_number_of_hours_worked_for_day(job_title='Accountant (Supernatural Assets)', time_code='PRRC', weekday='2023-12-05') = 15

follow up question: Column 'weekday' failed validator number 0: <Check isin: isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])> failure case examples: [{'weekday': '2023-12-04'}, {'weekday': "get_number_of_hours_worked_for_day(job_title='Accountant (Supernatural Assets)"}, {'weekday': "get_number_of_hours_worked_for_day(job_title='Accountant (Supernatural Assets)"}]
expected column 'hours' to have type Float64, got String
23:05:05 | WARNING  | polars_llm - could not generate data after 3, restarting conversation
23:05:05 | INFO     | polars_llm - question: Fill in 3 days of timesheets for a Accountant (Supernatural Assets) who works roughly 26.25 per week. Only use time_codes from the following dataset:
time_code,time_code_description
INVH,Investigation Hours
PRRC,Paranormal Research Time
GHTM,Ghost Hunting Time
AASV,Assets Valuation and Storage Value
SMMS,Social Media Management for Occult
META,Metaphysical Event Time Allocation
EDUC,Education and Training Time
TTRN,Travel Time for Research Narratives
OOCV,Office Overhead Costs Valuation

If an employee works multiple time codes in one day, they should be on separate rows. Do not produce more than 6 rows.
23:05:19 | WARNING  | polars_llm - bad attempt! num_attempts=1, num_retries=1

reply:
2023-11-27,invh,7.0
"2023-11-28","PRRC",11.0
"2023-11-29","GHTM",11.0
"2023-11-30","AASV",10.0
"2023-12-01","SMMS",2.0
"2023-12-04","META",4.0

follow up question: The first row did not look correct. It should only have the column names: hours,weekday,time_code
23:05:25 | WARNING  | polars_llm - bad attempt! num_attempts=1, num_retries=2

reply:
hours,weekday,time_code
"6.25","2023-12-04", "AASV"
"10","2023-11-28","PRRC"
"8","2023-11-29","GHTM"
"9","2023-11-30","META"
"4","2023-12-01","SMMS"
"6.25","2023-11-27", "INVH"

follow up question: Column 'weekday' failed validator number 0: <Check isin: isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])> failure case examples: [{'weekday': '2023-12-04'}, {'weekday': '2023-11-28'}, {'weekday': '2023-11-29'}, {'weekday': '2023-11-30'}, {'weekday': '2023-12-01'}]
23:05:31 | INFO     | polars_llm - success after num_retries=2, num_attempts=1! generated: shape: (6, 3)
┌───────┬───────────┬───────────┐
│ hours ┆ weekday   ┆ time_code │
│ ---   ┆ ---       ┆ ---       │
│ f64   ┆ str       ┆ str       │
╞═══════╪═══════════╪═══════════╡
│ 6.25  ┆ Monday    ┆ AASV      │
│ 10.0  ┆ Tuesday   ┆ PRRC      │
│ 8.0   ┆ Wednesday ┆ GHTM      │
│ 9.0   ┆ Thursday  ┆ META      │
│ 4.0   ┆ Friday    ┆ SMMS      │
│ 6.25  ┆ Monday    ┆ INVH      │
└───────┴───────────┴───────────┘
23:05:31 | INFO     | polars_llm - question: Fill in 3 days of timesheets for a Social Media Manager (Occult) who works roughly 8.75 per week. Only use time_codes from the following dataset:
time_code,time_code_description
INVH,Investigation Hours
PRRC,Paranormal Research Time
GHTM,Ghost Hunting Time
AASV,Assets Valuation and Storage Value
SMMS,Social Media Management for Occult
META,Metaphysical Event Time Allocation
EDUC,Education and Training Time
TTRN,Travel Time for Research Narratives
OOCV,Office Overhead Costs Valuation

If an employee works multiple time codes in one day, they should be on separate rows. Do not produce more than 6 rows.
23:05:46 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=1

reply:
weekday,employee,time_code,hours
2023-12-04,Social Media Manager (Occult),SMMS,4.0
2023-12-05,Social Media Manager (Occult),META,9.0
2023-12-06,Social Media Manager (Occult),PRRC,7.5
2023-12-07,Social Media Manager (Occult),INVH,6.0
2023-12-08,Social Media Manager (Occult),TTRN,1.0

follow up question: Column 'weekday' failed validator number 0: <Check isin: isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])> failure case examples: [{'weekday': '2023-12-04'}, {'weekday': '2023-12-05'}, {'weekday': '2023-12-06'}, {'weekday': '2023-12-07'}, {'weekday': '2023-12-08'}]
23:05:54 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=2

reply:
weekday,employee,time_code,hours
2023-12-04,Monday,Social Media Manager (Occult),SMMS,4.0
2023-12-05,Tuesday,Social Media Manager (Occult),META,9.0
2023-12-06,Wednesday,Social Media Manager (Occult),PRRC,7.5
2023-12-07,Thursday,Social Media Manager (Occult),INVH,6.0
2023-12-08,Friday,Social Media Manager (Occult),TTRN,1.0
2023-12-09,Saturday,Social Media Manager (Occult),PRRC,4.0

follow up question: Some lines had an incorrect amount of delimiters!
23:06:01 | INFO     | polars_llm - success after num_retries=2, num_attempts=0! generated: shape: (6, 3)
┌───────┬───────────┬───────────┐
│ hours ┆ weekday   ┆ time_code │
│ ---   ┆ ---       ┆ ---       │
│ f64   ┆ str       ┆ str       │
╞═══════╪═══════════╪═══════════╡
│ 4.0   ┆ Monday    ┆ SMMS      │
│ 9.0   ┆ Tuesday   ┆ META      │
│ 7.5   ┆ Wednesday ┆ PRRC      │
│ 6.0   ┆ Thursday  ┆ INVH      │
│ 1.0   ┆ Friday    ┆ TTRN      │
│ 4.75  ┆ Saturday  ┆ SMMS      │
└───────┴───────────┴───────────┘
23:06:01 | INFO     | basis - shape: (26, 4)
┌───────┬───────────┬───────────┬───────────────┐
│ hours ┆ weekday   ┆ time_code ┆ employee_code │
│ ---   ┆ ---       ┆ ---       ┆ ---           │
│ f64   ┆ str       ┆ str       ┆ str           │
╞═══════╪═══════════╪═══════════╪═══════════════╡
│ 7.92  ┆ Tuesday   ┆ PRRC      ┆ A-001         │
│ 2.0   ┆ Wednesday ┆ GHTM      ┆ A-001         │
│ 14.0  ┆ Thursday  ┆ AASV      ┆ A-001         │
│ 6.25  ┆ Friday    ┆ SMMS      ┆ A-001         │
│ 8.75  ┆ Saturday  ┆ META      ┆ A-001         │
│ …     ┆ …         ┆ …         ┆ …             │
│ 9.0   ┆ Tuesday   ┆ META      ┆ A-005         │
│ 7.5   ┆ Wednesday ┆ PRRC      ┆ A-005         │
│ 6.0   ┆ Thursday  ┆ INVH      ┆ A-005         │
│ 1.0   ┆ Friday    ┆ TTRN      ┆ A-005         │
│ 4.75  ┆ Saturday  ┆ SMMS      ┆ A-005         │
└───────┴───────────┴───────────┴───────────────┘
23:06:01 | INFO     | basis - generating payroll_definitions...
23:06:01 | INFO     | polars_llm - question: Generate a paycode mapping file that we can use to set up a payroll system for a Occult Detective Agency company. This should include all paycodes we would expect to pay to our employees. Include codes for ordinary, overtime, and holiday rates. Different leave types should use different pay codes. There should be at least 8 different paycodes.
23:06:05 | INFO     | polars_llm - success after num_retries=0, num_attempts=0! generated: shape: (8, 3)
┌──────────┬──────────────┬───────────────────────────────┐
│ pay_code ┆ pay_category ┆ pay_code_description          │
│ ---      ┆ ---          ┆ ---                           │
│ str      ┆ str          ┆ str                           │
╞══════════╪══════════════╪═══════════════════════════════╡
│ ORD      ┆ SAL          ┆ Ordinary Rate                 │
│ OT1      ┆ OTR          ┆ Overtime (x1.5)               │
│ HT1      ┆ HOL          ┆ Holiday Pay (x2.0)            │
│ SAL      ┆ SAL          ┆ Annual Salary                 │
│ LVL      ┆ LWP          ┆ Leave Without Pay             │
│ SLV      ┆ LWP          ┆ Sick Leave                    │
│ HBP      ┆ LWP          ┆ Household Business Paid Leave │
│ JUR      ┆ OTR          ┆ Judicial Review Pay           │
└──────────┴──────────────┴───────────────────────────────┘
23:06:05 | INFO     | basis - generating payroll...
23:06:05 | INFO     | polars_llm - question: Generate one week's worth of payroll data for a Full-time Occult Investigator who works 35.0 hours per week. Only use pay_codes from the following dataset:
pay_code,pay_code_description
ORD,Ordinary Rate
OT1,Overtime (x1.5)
HT1,Holiday Pay (x2.0)
SAL,Annual Salary
LVL,Leave Without Pay
SLV,Sick Leave
HBP,Household Business Paid Leave
JUR,Judicial Review Pay

Avoid having multiple rows with the same 'pay_code' or 'amount' values
23:06:16 | INFO     | polars_llm - success after num_retries=0, num_attempts=0! generated: shape: (4, 3)
┌──────────┬───────┬────────┐
│ pay_code ┆ hours ┆ amount │
│ ---      ┆ ---   ┆ ---    │
│ str      ┆ f64   ┆ f64    │
╞══════════╪═══════╪════════╡
│ HT1      ┆ 30.0  ┆ 60.0   │
│ JUR      ┆ 1.0   ┆ 250.0  │
│ ORD      ┆ 4.0   ┆ 70.0   │
│ OT1      ┆ 0.0   ┆ 0.0    │
└──────────┴───────┴────────┘
23:06:16 | INFO     | polars_llm - question: Generate one week's worth of payroll data for a Part-time Paranormal Researcher who works 17.5 hours per week. Only use pay_codes from the following dataset:
pay_code,pay_code_description
ORD,Ordinary Rate
OT1,Overtime (x1.5)
HT1,Holiday Pay (x2.0)
SAL,Annual Salary
LVL,Leave Without Pay
SLV,Sick Leave
HBP,Household Business Paid Leave
JUR,Judicial Review Pay

Avoid having multiple rows with the same 'pay_code' or 'amount' values
23:06:21 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=1

reply:
hourly_wage,_pay_code_=_calculate_hourly_wage(typical_monthly_salary=21435,_hours_per_week=17.5)
generate_payroll_data(hourly_wage= hourly_wage, pay_code="ORD", hours=hours_per_week)

follow up question: The first row did not look correct. It should only have the column names: pay_code,hours,amount
23:06:24 | INFO     | polars_llm - success after num_retries=1, num_attempts=0! generated: shape: (1, 3)
┌──────────┬───────┬────────┐
│ pay_code ┆ hours ┆ amount │
│ ---      ┆ ---   ┆ ---    │
│ str      ┆ f64   ┆ f64    │
╞══════════╪═══════╪════════╡
│ ORD      ┆ 17.0  ┆ 306.75 │
└──────────┴───────┴────────┘
23:06:24 | INFO     | polars_llm - question: Generate one week's worth of payroll data for a Full-time Ghost Hunter who works 35.0 hours per week. Only use pay_codes from the following dataset:
pay_code,pay_code_description
ORD,Ordinary Rate
OT1,Overtime (x1.5)
HT1,Holiday Pay (x2.0)
SAL,Annual Salary
LVL,Leave Without Pay
SLV,Sick Leave
HBP,Household Business Paid Leave
JUR,Judicial Review Pay

Avoid having multiple rows with the same 'pay_code' or 'amount' values
23:06:27 | INFO     | polars_llm - success after num_retries=0, num_attempts=0! generated: shape: (1, 3)
┌──────────┬───────┬────────┐
│ pay_code ┆ hours ┆ amount │
│ ---      ┆ ---   ┆ ---    │
│ str      ┆ f64   ┆ f64    │
╞══════════╪═══════╪════════╡
│ ORD      ┆ 35.0  ┆ 1092.0 │
└──────────┴───────┴────────┘
23:06:27 | INFO     | polars_llm - question: Generate one week's worth of payroll data for a Contract Accountant (Supernatural Assets) who works 26.25 hours per week. Only use pay_codes from the following dataset:
pay_code,pay_code_description
ORD,Ordinary Rate
OT1,Overtime (x1.5)
HT1,Holiday Pay (x2.0)
SAL,Annual Salary
LVL,Leave Without Pay
SLV,Sick Leave
HBP,Household Business Paid Leave
JUR,Judicial Review Pay

Avoid having multiple rows with the same 'pay_code' or 'amount' values
23:06:49 | INFO     | polars_llm - success after num_retries=0, num_attempts=0! generated: shape: (30, 3)
┌────────────┬────────┬────────┐
│ pay_code   ┆ hours  ┆ amount │
│ ---        ┆ ---    ┆ ---    │
│ str        ┆ f64    ┆ f64    │
╞════════════╪════════╪════════╡
│ 2023-12-01 ┆ 26.25  ┆ 625.0  │
│ 2023-12-02 ┆ 0.0    ┆ 0.0    │
│ 2023-12-03 ┆ 26.25  ┆ 625.0  │
│ 2023-12-04 ┆ 0.0    ┆ 0.0    │
│ 2023-12-05 ┆ 39.375 ┆ 937.5  │
│ …          ┆ …      ┆ …      │
│ 2023-12-26 ┆ 26.25  ┆ 625.0  │
│ 2023-12-27 ┆ 13.125 ┆ 312.5  │
│ 2023-12-28 ┆ 52.5   ┆ 1875.0 │
│ 2023-12-29 ┆ 0.0    ┆ 0.0    │
│ 2023-12-30 ┆ 78.75  ┆ 2812.5 │
└────────────┴────────┴────────┘
23:06:49 | INFO     | polars_llm - question: Generate one week's worth of payroll data for a Part-time Social Media Manager (Occult) who works 8.75 hours per week. Only use pay_codes from the following dataset:
pay_code,pay_code_description
ORD,Ordinary Rate
OT1,Overtime (x1.5)
HT1,Holiday Pay (x2.0)
SAL,Annual Salary
LVL,Leave Without Pay
SLV,Sick Leave
HBP,Household Business Paid Leave
JUR,Judicial Review Pay

Avoid having multiple rows with the same 'pay_code' or 'amount' values
23:07:00 | INFO     | polars_llm - success after num_retries=0, num_attempts=0! generated: shape: (1, 3)
┌──────────┬───────┬────────┐
│ pay_code ┆ hours ┆ amount │
│ ---      ┆ ---   ┆ ---    │
│ str      ┆ f64   ┆ f64    │
╞══════════╪═══════╪════════╡
│ ORD      ┆ 8.75  ┆ 109.4  │
└──────────┴───────┴────────┘
23:07:00 | INFO     | basis - shape: (37, 4)
┌────────────┬────────┬────────┬───────────────┐
│ pay_code   ┆ hours  ┆ amount ┆ employee_code │
│ ---        ┆ ---    ┆ ---    ┆ ---           │
│ str        ┆ f64    ┆ f64    ┆ str           │
╞════════════╪════════╪════════╪═══════════════╡
│ HT1        ┆ 30.0   ┆ 60.0   ┆ A-001         │
│ JUR        ┆ 1.0    ┆ 250.0  ┆ A-001         │
│ ORD        ┆ 4.0    ┆ 70.0   ┆ A-001         │
│ OT1        ┆ 0.0    ┆ 0.0    ┆ A-001         │
│ ORD        ┆ 17.0   ┆ 306.75 ┆ A-002         │
│ …          ┆ …      ┆ …      ┆ …             │
│ 2023-12-27 ┆ 13.125 ┆ 312.5  ┆ A-004         │
│ 2023-12-28 ┆ 52.5   ┆ 1875.0 ┆ A-004         │
│ 2023-12-29 ┆ 0.0    ┆ 0.0    ┆ A-004         │
│ 2023-12-30 ┆ 78.75  ┆ 2812.5 ┆ A-004         │
│ ORD        ┆ 8.75   ┆ 109.4  ┆ A-005         │
└────────────┴────────┴────────┴───────────────┘
23:07:00 | INFO     | basis - generating products...
23:07:00 | INFO     | polars_llm - question: Generate a variety of products our Occult Detective Agency company can sell on our website and eBay store. It should have a good mix of different items, styles  and themes. The 'product_description' field should be kept to one sentence. Each product_category should have more than one product. Generate at least 4 different products.
23:07:08 | WARNING  | polars_llm - bad attempt! num_attempts=0, num_retries=1

reply:
product_category,product_name,product_description,price,cost_materials
"Magical Tools","Crystal Ball, Golden Dawn Edition",A high-quality crystal ball perfect for scrying and divination,19.99,12.50
"Magical Tools","Witches' Brew Potion Kit",Create your own magical potions with this comprehensive kit,29.99,18.75
"Occult Literature","The Book of Lies by Aleister Crowley",A classic book on magical theory and practice,14.99,10.00
"Occult Literature","The Secret Teachings of All Ages by Manly P. Hall",A comprehensive guide to the mysteries of the ages,24.99,15.00
"Mystical Art","Sacred Geometry Print, Flower of Life",A beautiful print featuring sacred geometric patterns,19.99,12.50
"Occult Curiosities","Rare Tarot Card Deck, 1920s Edition",A vintage tarot card deck with intricate illustrations,49.99,25.00
"Mystical Art","Crystal Grid Kit for Manifestation",Create your own crystal grid for manifestation and energy work,39.99,20.00"

follow up question: There were some lines with an odd number of quotation marks, please only quote string fields.
23:07:16 | INFO     | polars_llm - success after num_retries=1, num_attempts=0! generated: shape: (7, 5)
┌────────────────┬────────────────────┬─────────────────────────────────┬───────┬─────────────────────────────────┐
│ cost_materials ┆ product_category   ┆ product_description             ┆ price ┆ product_name                    │
│ ---            ┆ ---                ┆ ---                             ┆ ---   ┆ ---                             │
│ f64            ┆ str                ┆ str                             ┆ f64   ┆ str                             │
╞════════════════╪════════════════════╪═════════════════════════════════╪═══════╪═════════════════════════════════╡
│ 12.5           ┆ Magical Tools      ┆ A high-quality crystal ball pe… ┆ 19.99 ┆ Crystal Ball,Golden Dawn Editi… │
│ 18.75          ┆ Magical Tools      ┆ Create your own magical potion… ┆ 29.99 ┆ Witches' Brew Potion Kit        │
│ 10.0           ┆ Occult Literature  ┆ A classic book on magical theo… ┆ 14.99 ┆ The Book of Lies by Aleister C… │
│ 15.0           ┆ Occult Literature  ┆ A comprehensive guide to the m… ┆ 24.99 ┆ The Secret Teachings of All Ag… │
│ 12.5           ┆ Mystical Art       ┆ A beautiful print featuring sa… ┆ 19.99 ┆ Sacred Geometry Print,Flower o… │
│ 25.0           ┆ Occult Curiosities ┆ A vintage tarot card deck with… ┆ 49.99 ┆ Rare Tarot Card Deck,1920s Edi… │
│ 20.0           ┆ Mystical Art       ┆ Create your own crystal grid f… ┆ 39.99 ┆ Crystal Grid Kit for Manifesta… │
└────────────────┴────────────────────┴─────────────────────────────────┴───────┴─────────────────────────────────┘
```
