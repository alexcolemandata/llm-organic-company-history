# llm-organic-company-history

A learning project to see how llms can work within a python environment.

## Idea: Organically Create a Company History using LLM agents

construct a history of a company using llms, in a 'stage-based' approach which
simulates the passage of time

## Generating data for a Knitting Company

```
> python -m organic_company_history.basis
```

```
created model ac-knitting-hr using llama3.1
created model ac-knitting-paycode using llama3.1
created model ac-timesheet-admin using llama3.1
created model ac-timesheet-peon using llama3.1
created model ac-knitting-payroll using llama3.1
created model ac-knitting-product using llama3.1


generating hr_data...
shape: (5, 8)
┌───────────────┬─────────────────────┬──────────────┬──────┬───────────────┬────────────────────┬───────────────┬──────────────┐
│ name          ┆ department          ┆ hire_date    ┆ fte  ┆ employee_code ┆ job_title          ┆ contract_type ┆ weekly_hours │
│ ---           ┆ ---                 ┆ ---          ┆ ---  ┆ ---           ┆ ---                ┆ ---           ┆ ---          │
│ str           ┆ str                 ┆ datetime[μs] ┆ f64  ┆ str           ┆ str                ┆ str           ┆ f64          │
╞═══════════════╪═════════════════════╪══════════════╪══════╪═══════════════╪════════════════════╪═══════════════╪══════════════╡
│ Emily Wilson  ┆ Knitting Department ┆ 2020-02-14   ┆ 1.0  ┆ E001          ┆ Senior Knitwear    ┆ Full-time     ┆ 35.0         │
│               ┆                     ┆ 00:00:00     ┆      ┆               ┆ Designer           ┆               ┆              │
│ Ryan Thompson ┆ Weaving Department  ┆ 2019-09-10   ┆ 0.75 ┆ E002          ┆ Assistant Weaver   ┆ Part-time     ┆ 26.25        │
│               ┆                     ┆ 00:00:00     ┆      ┆               ┆                    ┆               ┆              │
│ Sophia Patel  ┆ Yarn Production     ┆ 2018-05-20   ┆ 0.5  ┆ E003          ┆ Quality Control    ┆ Contract      ┆ 17.5         │
│               ┆ Department          ┆ 00:00:00     ┆      ┆               ┆ Specialist         ┆               ┆              │
│ David Lee     ┆ Knitting Department ┆ 2022-01-18   ┆ 1.0  ┆ E004          ┆ Junior Knitwear    ┆ Internship    ┆ 35.0         │
│               ┆                     ┆ 00:00:00     ┆      ┆               ┆ Developer          ┆               ┆              │
│ Ava Kim       ┆ Finishing           ┆ 2021-08-25   ┆ 0.75 ┆ E005          ┆ Finishing Line     ┆ Temporary     ┆ 26.25        │
│               ┆ Department          ┆ 00:00:00     ┆      ┆               ┆ Manager            ┆               ┆              │
└───────────────┴─────────────────────┴──────────────┴──────┴───────────────┴────────────────────┴───────────────┴──────────────┘


generating paycode_data...
shape: (10, 3)
┌────────────────────────┬──────────────┬──────────┐
│ pay_code_description   ┆ pay_category ┆ pay_code │
│ ---                    ┆ ---          ┆ ---      │
│ str                    ┆ str          ┆ str      │
╞════════════════════════╪══════════════╪══════════╡
│ Ordinary Hours Rate    ┆ Regular      ┆ ORI      │
│ Overtime Rate          ┆ Regular      ┆ OTR      │
│ Holiday Pay Rate       ┆ Regular      ┆ HOL      │
│ Paid Public Holiday    ┆ Leave        ┆ PPL      │
│ Paid Annual Sick Leave ┆ Leave        ┆ PAS      │
│ Paid Parental Leave    ┆ Leave        ┆ PAD      │
│ JobKeeper Payment      ┆ Special      ┆ JOM      │
│ Sick Leave Hours       ┆ Leave        ┆ SLH      │
│ Shiftwork Hours        ┆ Regular      ┆ SHR      │
│ Hours of Service Pay   ┆ Regular      ┆ HOS      │
└────────────────────────┴──────────────┴──────────┘


generating timesheet_codes...
shape: (8, 3)
┌───────────┬─────────────────────┬─────────────────────────────────┐
│ time_code ┆ time_category       ┆ time_code_description           │
│ ---       ┆ ---                 ┆ ---                             │
│ str       ┆ str                 ┆ str                             │
╞═══════════╪═════════════════════╪═════════════════════════════════╡
│ DKT       ┆ Product Development ┆ Designing Knitwear Togs         │
│ CKT       ┆ Product Development ┆ Creating Knitwear Templates     │
│ TKT       ┆ Product Development ┆ Testing Knitwear Samples        │
│ TWI       ┆ Production          ┆ Weaving Yarn                    │
│ FTW       ┆ Production          ┆ Finishing Woven Fabric          │
│ QC1       ┆ Quality Assurance   ┆ Inspecting Finished Products    │
│ JMDT      ┆ Product Development ┆ Developing New Knitwear Design… │
│ FNM1      ┆ Production          ┆ Managing Finishing Line Operat… │
└───────────┴─────────────────────┴─────────────────────────────────┘


generating timesheets...
shape: (42, 4)
┌───────────┬───────────┬───────┬───────────────┐
│ weekday   ┆ time_code ┆ hours ┆ employee_code │
│ ---       ┆ ---       ┆ ---   ┆ ---           │
│ str       ┆ str       ┆ f64   ┆ str           │
╞═══════════╪═══════════╪═══════╪═══════════════╡
│ Monday    ┆ DKT       ┆ 8.0   ┆ E001          │
│ Monday    ┆ CKT       ┆ 4.0   ┆ E001          │
│ Tuesday   ┆ TKT       ┆ 5.0   ┆ E001          │
│ Tuesday   ┆ TWI       ┆ 2.0   ┆ E001          │
│ Wednesday ┆ FTW       ┆ 6.0   ┆ E001          │
│ …         ┆ …         ┆ …     ┆ …             │
│ Thursday  ┆ QC1       ┆ 4.5   ┆ E005          │
│ Thursday  ┆ TKT       ┆ 2.75  ┆ E005          │
│ Friday    ┆ DKT       ┆ 3.25  ┆ E005          │
│ Saturday  ┆ CYT       ┆ 0.0   ┆ E005          │
│ Sunday    ┆ FNM1      ┆ 4.0   ┆ E005          │
└───────────┴───────────┴───────┴───────────────┘


generating payroll_data...
shape: (32, 4)
┌───────┬────────┬──────────┬───────────────┐
│ hours ┆ amount ┆ pay_code ┆ employee_code │
│ ---   ┆ ---    ┆ ---      ┆ ---           │
│ f64   ┆ f64    ┆ str      ┆ str           │
╞═══════╪════════╪══════════╪═══════════════╡
│ 35.0  ┆ 200.0  ┆ ORI      ┆ E001          │
│ 6.5   ┆ 130.0  ┆ OTR      ┆ E001          │
│ 4.0   ┆ 80.0   ┆ HOL      ┆ E001          │
│ 1.0   ┆ 20.0   ┆ PPL      ┆ E001          │
│ 3.0   ┆ 60.0   ┆ PAS      ┆ E001          │
│ …     ┆ …      ┆ …        ┆ …             │
│ 2.0   ┆ 36.0   ┆ PAD      ┆ E004          │
│ 7.0   ┆ 210.0  ┆ JOM      ┆ E004          │
│ 3.0   ┆ 54.0   ┆ SLH      ┆ E004          │
│ 4.0   ┆ 72.0   ┆ SHR      ┆ E004          │
│ 26.25 ┆ 0.0    ┆ ORI      ┆ E005          │
└───────┴────────┴──────────┴───────────────┘


generating product_line...
shape: (8, 5)
┌──────────────────────────────┬───────┬────────────────┬─────────────────────────────────┬─────────────────────┐
│ product_name                 ┆ price ┆ cost_materials ┆ product_description             ┆ product_category    │
│ ---                          ┆ ---   ┆ ---            ┆ ---                             ┆ ---                 │
│ str                          ┆ f64   ┆ f64            ┆ str                             ┆ str                 │
╞══════════════════════════════╪═══════╪════════════════╪═════════════════════════════════╪═════════════════════╡
│ Knitted Baby Blanket         ┆ 39.99 ┆ 15.0           ┆ A soft and cozy knitted baby b… ┆ Baby                │
│ Colorful Market Bag          ┆ 29.99 ┆ 8.5            ┆ A vibrant and sturdy market ba… ┆ Home Decor          │
│ Handmade Scarf               ┆ 19.99 ┆ 5.25           ┆ A stylish and warm handmade sc… ┆ Fashion Accessories │
│ Personalized Sweater         ┆ 49.95 ┆ 20.0           ┆ A high-quality, personalized s… ┆ Fashion Apparel     │
│ Knitted Socks Set of 3       ┆ 14.99 ┆ 4.5            ┆ A set of three soft and cozy k… ┆ Footwear            │
│ Crocheted Coasters Set of 6  ┆ 9.95  ┆ 2.75           ┆ A set of six colorful crochete… ┆ Home Decor          │
│ Customized Fingerless Gloves ┆ 24.99 ┆ 7.0            ┆ A pair of warm and customized … ┆ Winter Accessories  │
│ Hand-Knitted Baby Booties    ┆ 12.99 ┆ 3.75           ┆ A pair of adorable hand-knitte… ┆ Baby Shoes          │
└──────────────────────────────┴───────┴────────────────┴─────────────────────────────────┴─────────────────────┘
```
