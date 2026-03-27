# Project to Syllabus Mapping (Topic-Wise)

This document maps the current implementation to a 1.1 to 6.7 syllabus-style structure for presentation use.

Status legend:
- Implemented: clearly used in runtime project flow.
- Partial: used in limited form, or only in notebook/auxiliary flow.
- Not used: not found in this codebase.

## 1. Python Programming Fundamentals

| Topic | Status | Where used in this project |
|---|---|---|
| 1.1 Variables, data types, operators | Implemented | Numeric and categorical computations in pipeline and analysis modules, e.g. aggregate variable calculations in pipeline/stage_03_transform.py |
| 1.2 Conditional logic and control flow | Implemented | Multiple validation branches and guards, e.g. routes/upload.py and routes/period_scope.py |
| 1.3 Loops and iteration patterns | Implemented | Iteration over endpoint definitions and table/chart rows in ecommerce_frontend/static_dashboard/js/dashboard.js |
| 1.4 Functions and modular decomposition | Implemented | Separate compute functions per analysis section in ecommerce_backend/analysis/*.py |
| 1.5 Lambda and functional style usage | Implemented | lambda usage in cleaning and aggregations, e.g. pipeline/stage_02_clean.py and analysis/products.py |
| 1.6 Decorators (framework and route decorators) | Implemented | FastAPI route decorators in routes/analysis.py, routes/report.py, routes/upload.py; startup decorator in main.py |
| 1.7 Iterables, generators, advanced Python constructs | Partial | Iterable typing usage and iterator-heavy processing exist; custom generators are not central to the current logic |

## 2. Data Collection, APIs, and Storage

| Topic | Status | Where used in this project |
|---|---|---|
| 2.1 Reading structured data files (Excel) | Implemented | Excel ingestion in pipeline/stage_01_ingest.py and upload flow in routes/upload.py |
| 2.2 Data validation and ingestion rules | Implemented | File-type validation and processing guards in routes/upload.py |
| 2.3 REST API design and consumption | Implemented | FastAPI backend endpoints in routes/analysis.py and routes/report.py; browser fetch client in ecommerce_frontend/static_dashboard/js/dashboard.js |
| 2.4 JSON payload construction and exchange | Implemented | API response payloads from analysis endpoints and frontend parsing in ecommerce_frontend/static_dashboard/js/dashboard.js |
| 2.5 Relational database integration (SQL/SQLite) | Implemented | SQLite connection, table management, merge, and load logic in ecommerce_backend/database.py |
| 2.6 Non-relational database usage (MongoDB/NoSQL) | Not used | No NoSQL connector or schema found |
| 2.7 SOAP/XML API integration or web scraping pipeline | Not used | No SOAP client, XML workflow, or scraping framework detected |

## 3. Data Cleaning, Wrangling, and Pipeline Engineering

| Topic | Status | Where used in this project |
|---|---|---|
| 3.1 Merge, join, reshape, and grouping operations | Implemented | merge/join/groupby in analysis/inventory.py and analysis/products.py; reshape evidence in notebook unstack in notebooks/Nepal_Ecommerce_BI_2025.ipynb |
| 3.2 Missing value handling and data quality checks | Implemented | Median/mode imputation and invalid row filtering in pipeline/stage_02_clean.py |
| 3.3 Categorical and time-series transformations | Implemented | Date parsing and Month/Year feature creation in pipeline/stage_02_clean.py and notebook |
| 3.4 Feature transformation, encoding, scaling | Partial | Derived feature creation is strong; explicit ML scaling/encoding pipelines are not a major runtime component |
| 3.5 Memory optimization and large-data chunk/lazy processing | Not used | No chunked/lazy read strategy or explicit memory optimization pattern found |
| 3.6 Reusable cleaning utilities and helper methods | Implemented | Reusable helper functions in pipeline/stage_02_clean.py |
| 3.7 Multi-stage data pipeline orchestration | Implemented | Three-stage runner design in pipeline/runner.py with stage_01_ingest.py, stage_02_clean.py, stage_03_transform.py |

## 4. Applied Statistics and Business Metrics

| Topic | Status | Where used in this project |
|---|---|---|
| 4.1 Descriptive statistics (mean/median/quantile summaries) | Implemented | Quantile and mean usage in notebook, plus aggregate KPIs in analysis modules and transform stage |
| 4.2 Ratio metrics and KPI engineering | Implemented | Profit margins, discount share, turnover, growth percentages in analysis/*.py |
| 4.3 Correlation/covariance/skewness/kurtosis analysis | Partial | Limited exploratory traces in notebook; no strong runtime endpoint dedicated to these statistics |
| 4.4 Hypothesis testing and inferential statistics | Not used | No t-test/chi-square/ANOVA hypothesis workflow in project runtime |
| 4.5 Regression/statistical modeling (statsmodels/scipy) | Not used | No statsmodels/scipy model workflow in backend logic |
| 4.6 Break-even and cashflow analytical models | Implemented | Dedicated modules analysis/breakeven.py and analysis/cashflow.py |
| 4.7 Time-bucket business trend analysis | Implemented | Monthly/quarterly/semiannual/annual support in routes/period_scope.py and growth/cashflow routes |

## 5. Visualization, Reporting, and Storytelling

| Topic | Status | Where used in this project |
|---|---|---|
| 5.1 Frontend charting and dashboard visuals | Implemented | ApexCharts-based dashboards in ecommerce_frontend/static_dashboard/js/dashboard.js |
| 5.2 Notebook EDA visualization (matplotlib/seaborn) | Implemented | Imports and chart cells in notebooks/Nepal_Ecommerce_BI_2025.ipynb |
| 5.3 Interactive filtering and scoped exploration | Implemented | period and bucket filtering from frontend UI to backend endpoints; logic in routes/period_scope.py |
| 5.4 Tabular views and search/filter UX | Implemented | Client-side table filters in dashboard.js |
| 5.5 PDF report generation | Implemented | PDF generation in reports/report_generator.py and endpoint in routes/report.py |
| 5.6 Excel report generation | Implemented | Excel export in reports/report_generator.py and endpoint in routes/report.py |
| 5.7 Plotly or advanced BI embedding | Not used | No Plotly integration in runtime frontend or backend |

## 6. Software Engineering, Deployment, and Automation

| Topic | Status | Where used in this project |
|---|---|---|
| 6.1 Modular architecture and separation of concerns | Implemented | Clear separation into routes, pipeline, analysis, reports, database, frontend services |
| 6.2 Logging and observability basics | Implemented | Central logger with usage across modules, e.g. logger.py and route/pipeline logs |
| 6.3 Error handling and API resilience | Implemented | HTTP exceptions and graceful frontend partial-failure handling in ecommerce_frontend/static_dashboard/js/dashboard.js |
| 6.4 Concurrency and parallel I/O tasks | Implemented | Promise.all-based parallel endpoint fetching in ecommerce_frontend/static_dashboard/js/dashboard.js |
| 6.5 Scheduling/background jobs | Not used | No scheduler (cron/celery/apscheduler) present |
| 6.6 Startup bootstrap and data lifecycle automation | Implemented | Startup bootstrap from raw files and SQLite state loading in main.py and database.py |
| 6.7 Production deployment and CI/CD pipeline | Partial | Local run scripts and app structure exist; no full CI/CD workflow files found |

## Presentation Notes (Quick Script)

- Strongest implemented areas:
  - ETL-style data pipeline with cleaning and transformations.
  - REST API analytics service plus scoped period filtering.
  - Relational persistence with SQLite and merge-dedup workflow.
  - Dashboard visualization and report exports (PDF, Excel).

- Clearly partial/not-used areas to mention transparently:
  - No SOAP/scraping/NoSQL stack.
  - No formal inferential statistics or statsmodels regression endpoints.
  - No scheduler-based automation or complete CI/CD pipeline.

- Recommended phrasing during demo:
  - "Implemented deeply" for pipeline, API, KPI computation, dashboarding, and reporting.
  - "Partially covered" for advanced stats and production engineering.
  - "Not in current scope" for SOAP, scraping, NoSQL, scheduling, and Plotly runtime integration.
