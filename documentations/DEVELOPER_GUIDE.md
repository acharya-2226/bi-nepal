# Developer Guide: End-to-End Data and Display Flow

## Scope
This document explains how data is accepted, processed, persisted, analyzed, and displayed in the frontend.

## High-Level Architecture
- Backend: FastAPI (`ecommerce_backend`)
- Frontend: static HTML/CSS/JS dashboard (`ecommerce_frontend/static_dashboard`)
- Storage: SQLite (`ecommerce_backend/data/app.db`)
- Shared contract: JSON endpoints under `/analysis/*` and file exports under `/report/*`

## Runtime Ports
Using `start_frontend_backend.bat`:
- FastAPI backend: `http://127.0.0.1:8002`
- Static frontend: `http://127.0.0.1:8010`

The static page reads backend base URL from the UI input (`API Base URL`) and stores it in browser localStorage.

## Startup Behavior (Backend)
File: `ecommerce_backend/main.py`

1. Initialize logging and SQLite.
2. Attempt to load complete dataset from SQLite using `load_store()`.
3. If DB is ready, populate `state.store` and serve analysis immediately.
4. If DB is empty, bootstrap from legacy Excel files in `ecommerce_backend/data/raw`:
   - run pipeline per file,
   - merge into SQLite,
   - reload `state.store` from DB.

## Data Ingestion Path (Upload)
File: `ecommerce_backend/routes/upload.py`

`POST /upload` flow:
1. Validate file extension (`.xlsx`/`.xls`).
2. Save file into `data/raw`.
3. Run `run_pipeline(file_path)`.
4. Persist processed frames via `merge_context(context, source_filename)`.
5. Refresh runtime cache: `state.store.update(load_store())`.
6. Return success JSON.

## Pipeline Internals
### Stage 1: Ingest
File: `ecommerce_backend/pipeline/stage_01_ingest.py`

- Reads required sheets: Inventory, Sales, Purchase, Expenses.
- Stores raw DataFrames in context keys: `inv`, `sales`, `purch`, `exp`.

### Stage 2: Clean
File: `[ecommerce_backend/pipeline/stage_02_clean.py]`

Main operations:
- normalize column names and trim text fields,
- parse date columns,
- coerce numeric columns,
- impute missing values (mode for categorical, median for numeric),
- conditional fill for sales `DeliveryCharge` based on `DeliveryType`,
- remove invalid transaction rows,
- remove duplicates,
- derive time columns (`Month`, `Year`, `MonthName`, `MonthNum`).

### Stage 3: Transform
File: `ecommerce_backend/pipeline/stage_03_transform.py`

Computes shared derived metrics into `context["vars"]`, including:
- quantity totals,
- gross/net revenue,
- discounts,
- weighted average cost,
- COGS,
- total operating expense.

These values are reused across analysis modules.

## Persistence and State Model
File: `ecommerce_backend/database.py`

- SQLite tables: `inv`, `sales`, `purch`, `exp`, `upload_log`.
- Merge mode: append rows then dedupe by full-row equality (keep earliest `rowid`).
- `load_store()` reads all tables and rebuilds `vars` using `transform()`.

File: `ecommerce_backend/state.py`

- `state.store` acts as in-memory cache:
  - `inv`, `sales`, `purch`, `exp`, `vars`, `ready`

## Analysis API Layer
File: `ecommerce_backend/routes/analysis.py`

Endpoints:
- `/analysis/profitability`
- `/analysis/discounts`
- `/analysis/inventory`
- `/analysis/products`
- `/analysis/expenses`
- `/analysis/monthly-growth`
- `/analysis/breakeven`
- `/analysis/cashflow`

Processing pattern per request:
1. `_require_data()` checks `state.store["ready"]`.
2. `scoped_store()` applies period/bucket filtering.
3. Endpoint-specific `compute_*` function returns JSON.

## Period and Bucket Scoping
File: `ecommerce_backend/routes/period_scope.py`

- Supported `period`: monthly, quarterly, semiannual, annual.
- Optional `bucket`: month/quarter/half/year label or `all`.
- Converts bucket to set of month numbers.
- Filters sales/purchase/expense tables to selected months.
- Re-runs `transform()` on scoped subset before analysis.

## Report API Layer
File: `ecommerce_backend/routes/report.py`

- `/report/pdf` and `/report/excel` accept same `period`/`bucket` query params.
- Uses scoped store, then `generate_pdf()` / `generate_excel()`.
- Returns file response with no-cache headers.

## Frontend Data Fetch and Rendering
### Static Files
Files:
- `ecommerce_frontend/static_dashboard/index.html`
- `ecommerce_frontend/static_dashboard/css/styles.css`
- `ecommerce_frontend/static_dashboard/js/dashboard.js`

Rendering model:
1. Static HTML loads and initializes defaults (`period=monthly`, `bucket=all`).
2. JavaScript fetches all analysis endpoints in parallel using browser `fetch`.
3. API calls include query params `period` and optional `bucket`.
4. Response payload is rendered into KPI cards, tables, and ApexCharts charts.
5. Frontend keeps partial rendering even if some endpoints fail and displays errors in the panel.
6. Report links are built dynamically as `/report/pdf` and `/report/excel` with the same active scope.

## Sequence Summary
1. User uploads Excel via `POST /upload`.
2. FastAPI pipeline ingests, cleans, transforms.
3. Processed rows are merged into SQLite and deduped.
4. Runtime `state.store` is refreshed from DB.
5. Frontend requests `/analysis/*` endpoints with period/bucket.
6. Backend returns scoped analytics JSON.
7. Static JS renders dashboard cards/charts/tables from JSON.
8. Optional report download hits `/report/pdf` or `/report/excel`.

## Operational Notes for Developers
- Backend must be running before frontend can render complete data.
- If some analysis endpoints fail, frontend displays available sections and error list.
- If selected scope has no rows, backend returns 400 (`No data available for the selected period bucket.`).
- Full-row dedupe can retain semantically duplicate records if any non-key column differs.
- CORS is already permissive in backend (`allow_origins=["*"]`), so static frontend calls succeed across local ports.

## Suggested Engineering Improvements
1. Add strict schema validation for all required columns before pipeline stages.
2. Add automated tests for pipeline stages and API integration.
3. Add DB migration/versioning strategy.
4. Replace full-row dedupe with business-key upsert logic where available.
5. Add auth/rate-limiting for non-local deployment.
