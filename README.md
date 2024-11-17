# llm-organic-company-history

A learning project to see how llms can work within a python environment.

## Demo: Generating Data for an Occult Detective Agency

The 'main' script accepts the 'industry' as an input argument when run from the
command line.

For example: Generating data for an Occult Detecive Agency:

```
> python -m organic_company_history.main "occult detective"
```

```
Generating data for Occult Detective:

created model user/occult-detective/hr using llama3.1
created model user/occult-detective/payroll-admin using llama3.1
created model user/occult-detective/timesheet-admin using llama3.1
created model user/occult-detective/timesheet-peon using llama3.1
created model user/occult-detective/payroll-peon using llama3.1
created model user/occult-detective/product using llama3.1


generating hr...
shape: (5, 8)
┌────────────────────────────┬──────────────────────┬──────┬───────────────┬─────────────────────┬────────────────┬───────────────┬──────────────┐
│ department                 ┆ job_title            ┆ fte  ┆ employee_code ┆ hire_date           ┆ name           ┆ contract_type ┆ weekly_hours │
│ ---                        ┆ ---                  ┆ ---  ┆ ---           ┆ ---                 ┆ ---            ┆ ---           ┆ ---          │
│ str                        ┆ str                  ┆ f64  ┆ str           ┆ datetime[μs]        ┆ str            ┆ str           ┆ f64          │
╞════════════════════════════╪══════════════════════╪══════╪═══════════════╪═════════════════════╪════════════════╪═══════════════╪══════════════╡
│ Research and Investigation ┆ Occult Detective     ┆ 1.0  ┆ Alice13       ┆ 2020-02-01 00:00:00 ┆ Alice Jenkins  ┆ Full-time     ┆ 35.0         │
│ Paranormal Case Management ┆ Case Manager         ┆ 0.5  ┆ Bruno42       ┆ 2019-09-15 00:00:00 ┆ Bruno Thompson ┆ Part-time     ┆ 17.5         │
│ Cryptid Studies            ┆ Researcher           ┆ 1.0  ┆ Charlie19     ┆ 2022-05-20 00:00:00 ┆ Charlie Lee    ┆ Full-time     ┆ 35.0         │
│ Occult Artifact Analysis   ┆ Artifact Specialist  ┆ 0.75 ┆ Diana11       ┆ 2018-03-25 00:00:00 ┆ Diana Patel    ┆ Contract      ┆ 26.25        │
│ New Recruits and Training  ┆ Training Coordinator ┆ 0.0  ┆ Emily28       ┆ 2021-10-12 00:00:00 ┆ Emily Garcia   ┆ Internship    ┆ 0.0          │
└────────────────────────────┴──────────────────────┴──────┴───────────────┴─────────────────────┴────────────────┴───────────────┴──────────────┘


generating payroll_definitions...
shape: (11, 3)
┌──────────┬──────────────────────────┬──────────────┐
│ pay_code ┆ pay_code_description     ┆ pay_category │
│ ---      ┆ ---                      ┆ ---          │
│ str      ┆ str                      ┆ str          │
╞══════════╪══════════════════════════╪══════════════╡
│ HORR     ┆ Ordinary Hourly Rate     ┆ Hourly       │
│ OTHR     ┆ Overtime Hourly Rate     ┆ Hourly       │
│ HDLH     ┆ Holiday Hourly Rate      ┆ Hourly       │
│ SALR     ┆ Salaried Pay             ┆ Salary       │
│ BCKW     ┆ Back Pay                 ┆ Adjustment   │
│ …        ┆ …                        ┆ …            │
│ HEALTH   ┆ Health Insurance Premium ┆ Benefit      │
│ DENTL    ┆ Dental Insurance Premium ┆ Benefit      │
│ VACN     ┆ Vacation Pay             ┆ Leave        │
│ SICK     ┆ Sick Leave Pay           ┆ Leave        │
│ HOLI     ┆ Holiday Pay              ┆ Leave        │
└──────────┴──────────────────────────┴──────────────┘


generating timesheet_codes...
shape: (12, 3)
┌───────────┬───────────────┬───────────────────────┐
│ time_code ┆ time_category ┆ time_code_description │
│ ---       ┆ ---           ┆ ---                   │
│ str       ┆ str           ┆ str                   │
╞═══════════╪═══════════════╪═══════════════════════╡
│ OD1       ┆ Billable      ┆ Investigation         │
│ OD2       ┆ Billable      ┆ Interviews            │
│ OD3       ┆ Non-Billable  ┆ Research              │
│ OD4       ┆ Reimbursable  ┆ Travel                │
│ CM1       ┆ Non-Billable  ┆ Client Calls          │
│ …         ┆ …             ┆ …                     │
│ RSH       ┆ Reimbursable  ┆ Site Visits           │
│ AS1       ┆ Non-Billable  ┆ Inventory Management  │
│ AS2       ┆ Reimbursable  ┆ Conservation          │
│ TC1       ┆ Non-Billable  ┆ New Hire Onboarding   │
│ TC2       ┆ Billable      ┆ Compliance Training   │
└───────────┴───────────────┴───────────────────────┘


generating timesheets...
shape: (39, 4)
┌───────────┬───────────┬───────┬───────────────┐
│ time_code ┆ weekday   ┆ hours ┆ employee_code │
│ ---       ┆ ---       ┆ ---   ┆ ---           │
│ str       ┆ str       ┆ f64   ┆ str           │
╞═══════════╪═══════════╪═══════╪═══════════════╡
│ OD1       ┆ Monday    ┆ 8.75  ┆ Alice13       │
│ CM2       ┆ Monday    ┆ 5.0   ┆ Alice13       │
│ AS1       ┆ Monday    ┆ 4.25  ┆ Alice13       │
│ RSH       ┆ Tuesday   ┆ 9.0   ┆ Alice13       │
│ TC1       ┆ Tuesday   ┆ 6.0   ┆ Alice13       │
│ …         ┆ …         ┆ …     ┆ …             │
│ TC2       ┆ Wednesday ┆ 0.25  ┆ Emily28       │
│ RSC       ┆ Thursday  ┆ 0.0   ┆ Emily28       │
│ CM2       ┆ Friday    ┆ 0.125 ┆ Emily28       │
│ AS2       ┆ Saturday  ┆ 0.0   ┆ Emily28       │
│ TC1       ┆ Sunday    ┆ 0.0   ┆ Emily28       │
└───────────┴───────────┴───────┴───────────────┘


generating payroll...
shape: (48, 4)
┌──────────┬───────┬────────┬───────────────┐
│ pay_code ┆ hours ┆ amount ┆ employee_code │
│ ---      ┆ ---   ┆ ---    ┆ ---           │
│ str      ┆ f64   ┆ f64    ┆ str           │
╞══════════╪═══════╪════════╪═══════════════╡
│ HORR     ┆ 35.0  ┆ 1450.0 ┆ Alice13       │
│ OTHR     ┆ 10.0  ┆ 250.0  ┆ Alice13       │
│ HDLH     ┆ 8.0   ┆ 320.0  ┆ Alice13       │
│ SALR     ┆ 1.0   ┆ 3100.0 ┆ Alice13       │
│ BCKW     ┆ 5.0   ┆ 1250.0 ┆ Alice13       │
│ …        ┆ …     ┆ …      ┆ …             │
│ HEALTH   ┆ 0.0   ┆ 0.0    ┆ Emily28       │
│ DENTL    ┆ 0.0   ┆ 0.0    ┆ Emily28       │
│ VACN     ┆ 0.0   ┆ 0.0    ┆ Emily28       │
│ SICK     ┆ 0.0   ┆ 0.0    ┆ Emily28       │
│ HOLI     ┆ 0.0   ┆ 0.0    ┆ Emily28       │
└──────────┴───────┴────────┴───────────────┘


generating products...
shape: (8, 5)
┌──────────────────────┬─────────────────────────────────┬────────────────┬───────┬─────────────────────────────────┐
│ product_category     ┆ product_name                    ┆ cost_materials ┆ price ┆ product_description             │
│ ---                  ┆ ---                             ┆ ---            ┆ ---   ┆ ---                             │
│ str                  ┆ str                             ┆ f64            ┆ f64   ┆ str                             │
╞══════════════════════╪═════════════════════════════════╪════════════════╪═══════╪═════════════════════════════════╡
│ Magical Tools        ┆ Crystal Wand, Amethyst (10 inc… ┆ 15.99          ┆ 24.99 ┆ A handmade crystal wand imbued… │
│ Magical Tools        ┆ Witch's Altar Cloth, Black Vel… ┆ 4.99           ┆ 12.99 ┆ A luxurious black velvet altar… │
│ Occult Literature    ┆ The Key of Solomon, Hardcover … ┆ 9.99           ┆ 14.99 ┆ A rare and ancient grimoire co… │
│ Occult Literature    ┆ The Book of Enoch, Leather-Bou… ┆ 19.99          ┆ 29.99 ┆ A leather-bound edition of the… │
│ Curiosities & Relics ┆ Vintage Ouija Board (18x24 inc… ┆ 12.99          ┆ 19.99 ┆ A genuine vintage ouija board … │
│ Curiosities & Relics ┆ Taxidermied Raven, 10 inches t… ┆ 25.99          ┆ 39.99 ┆ A taxidermied raven with glass… │
│ Rare Artifacts       ┆ Anubis Figurine, Bronze (6 inc… ┆ 29.99          ┆ 49.99 ┆ A bronze figurine of Anubis, t… │
│ Rare Artifacts       ┆ Lammas Day Candle Set, Hand-Di… ┆ 14.99          ┆ 24.99 ┆ A set of hand-dipped candles i… │
└──────────────────────┴─────────────────────────────────┴────────────────┴───────┴─────────────────────────────────┘
```
