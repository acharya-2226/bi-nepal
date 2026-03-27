# Project Presentation Template Mapping (Where Implemented)

This file maps each presentation section to concrete implementation points in the codebase.

Path note: links in this file are relative to the `ecommerce_backend` folder.

## 1. Problem Definition and Objective
- Backend objective and API description:
  - App entrypoint and startup bootstrap: [main.py](main.py)
  - Project scope summary: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
- Analytics scope endpoints:
  - API route module: [routes/analysis.py](routes/analysis.py) (router, profitability, discounts, inventory, products, expenses, monthly_growth, breakeven, cashflow)

## 2. Dataset Description and Data Source
- Excel as source and expected sheet structure:
  - Ingestion function and sheet reads: [pipeline/stage_01_ingest.py](pipeline/stage_01_ingest.py)
  - Dataset contract documentation: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
- Persisted data source (SQLite):
  - DB connection/table merge/load logic: [database.py](database.py) (get_connection, init_db, merge_context, load_store)

## 3. Data Collection and Ingestion Method
- Upload and validation flow:
  - Upload endpoint and file validation: [routes/upload.py](routes/upload.py) (upload_file)
- Pipeline orchestration:
  - Pipeline runner module: [pipeline/runner.py](pipeline/runner.py) (run_pipeline)
- Startup bootstrap ingestion from raw files:
  - Startup event and raw-file bootstrap: [main.py](main.py) (startup)

## 4. Data Cleaning and Feature Engineering
- Missing values, type coercion, row filtering:
  - Cleaning module: [pipeline/stage_02_clean.py](pipeline/stage_02_clean.py) (clean and helper functions)
- Derived feature/metric construction:
  - Transform module: [pipeline/stage_03_transform.py](pipeline/stage_03_transform.py) (transform)

## 5. Data Analysis and Statistical Exploration
- Section-wise KPI computation:
  - Profitability: [analysis/profitability.py](analysis/profitability.py) (compute_profitability)
  - Discounts: [analysis/discounts.py](analysis/discounts.py) (compute_discounts)
  - Inventory: [analysis/inventory.py](analysis/inventory.py) (compute_inventory)
  - Products: [analysis/products.py](analysis/products.py) (compute_products)
  - Expenses: [analysis/expenses.py](analysis/expenses.py) (compute_expenses)
  - Growth: [analysis/monthly_growth.py](analysis/monthly_growth.py) (compute_monthly_growth)
  - Break-even: [analysis/breakeven.py](analysis/breakeven.py) (compute_breakeven)
  - Cashflow: [analysis/cashflow.py](analysis/cashflow.py) (compute_cashflow)
- Grouping/merge operations:
  - Groupby/join examples: [analysis/products.py](analysis/products.py)
  - Merge examples: [analysis/inventory.py](analysis/inventory.py)

## 6. Key Insights and Interpretation
- Insight-ready response objects returned from APIs:
  - Analysis route outputs: [routes/analysis.py](routes/analysis.py)
- Static dashboard consumption for interpretation:
  - Page composition and controls: [../ecommerce_frontend/static_dashboard/index.html](../ecommerce_frontend/static_dashboard/index.html)
  - Backend fetch/aggregation and rendering: [../ecommerce_frontend/static_dashboard/js/dashboard.js](../ecommerce_frontend/static_dashboard/js/dashboard.js)

## 7. Interactive Dashboard and Visualization
- Frontend visual rendering and interactions:
  - Chart and interaction logic: [../ecommerce_frontend/static_dashboard/js/dashboard.js](../ecommerce_frontend/static_dashboard/js/dashboard.js)
- Dashboard page and controls:
  - Dashboard page: [../ecommerce_frontend/static_dashboard/index.html](../ecommerce_frontend/static_dashboard/index.html)
- API fetch and concurrency for dashboard data:
  - Concurrent browser requests: [../ecommerce_frontend/static_dashboard/js/dashboard.js](../ecommerce_frontend/static_dashboard/js/dashboard.js) (Promise.all)

## 8. Technical Architecture and Project Structure
- Main app assembly and route registration:
  - App setup and router inclusion: [main.py](main.py)
- Modular package layout:
  - Routes package: [routes/](routes/)
  - Pipeline package: [pipeline/](pipeline/)
  - Analysis package: [analysis/](analysis/)
  - Reports package: [reports/](reports/)
- System overview documentation:
  - Architecture summary: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

## 9. Advanced Python Implementation
- Exception handling in API routes:
  - Upload exceptions: [routes/upload.py](routes/upload.py)
  - Report endpoint guards: [routes/report.py](routes/report.py)
- Logging setup and usage:
  - Logger setup module: [logger.py](logger.py)
  - Startup logging usage: [main.py](main.py)
- Concurrency:
  - Parallel request execution: [../ecommerce_frontend/static_dashboard/js/dashboard.js](../ecommerce_frontend/static_dashboard/js/dashboard.js) (Promise.all)
- Client-side state modeling:
  - State object and endpoint definitions: [../ecommerce_frontend/static_dashboard/js/dashboard.js](../ecommerce_frontend/static_dashboard/js/dashboard.js)

## 10. Conclusion and Future Scope
- Current deliverables and report export scope:
  - Report generation implementation: [reports/report_generator.py](reports/report_generator.py) (generate_pdf, generate_excel)
  - Report download endpoints: [routes/report.py](routes/report.py)
- Existing project summary baseline for conclusion slide:
  - Summary and scope narrative: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

---

## Quick Coverage Notes for Presentation
- Fully implemented now:
  - ETL-like pipeline, REST analytics APIs, SQLite persistence, dashboard visuals, PDF/Excel export.
- Partially implemented now:
  - Advanced statistical modeling and production-grade CI/CD.
- Not currently implemented:
  - NoSQL integration, SOAP/scraping pipelines, scheduler-based automation.
