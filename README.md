# Static Dashboard Frontend

This frontend is a static HTML/CSS/JS dashboard that consumes analytics from the FastAPI backend.
It does not require a frontend build step.

## What This Dashboard Does

- Connects to a configurable backend API base URL.
- Fetches all BI sections in parallel.
- Supports scoped analytics by period and bucket.
- Renders KPIs, charts, and summary panels.
- Downloads PDF and Excel reports for the active scope.
- Stores API base URL in browser localStorage for convenience.

## Default Local URLs

- Backend API: `http://127.0.0.1:8002`
- Frontend dashboard: `http://127.0.0.1:8010`
- Backend Swagger docs: `http://127.0.0.1:8002/docs`

## Fastest Start (Recommended)

From the workspace parent folder, run:

```bat
start_frontend_backend.bat
```

What this launcher does:

1. Verifies backend and frontend folders.
2. Creates backend `.venv` if missing.
3. Installs backend dependencies.
4. Frees ports `8002` and `8010` if in use.
5. Starts backend with Uvicorn on `127.0.0.1:8002`.
6. Starts static server on `127.0.0.1:8010`.
7. Opens the dashboard in your browser.

## Manual Start

### 1) Start backend

```powershell
cd ecommerce_backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8002
```

### 2) Serve static frontend

In a separate terminal:

```powershell
cd ecommerce_frontend
python -m http.server 8010 --bind 127.0.0.1 --directory static_dashboard
```

### 3) Open dashboard

Open: `http://127.0.0.1:8010`

## Data Flow (End to End)

1. Upload Excel workbook to backend (`POST /upload`) from Swagger UI.
2. Backend pipeline ingests, cleans, transforms, and persists to SQLite.
3. Backend refreshes in-memory store (`state.store`).
4. Frontend fetches scoped analytics from `/analysis/*` endpoints.
5. Frontend renders KPIs/charts/tables and enables report export.

## Required Upload Sheets

Your Excel workbook should contain these sheets:

- `Inventory`
- `Sales`
- `Purchase`
- `Expenses`

## Minimum Column Checklist

### Inventory
- `ItemID`
- `ItemName`
- `Category`
- `OpeningStock`
- `ReorderLevel`
- `SellingPrice`

### Sales
- `Date`
- `ItemID`
- `QuantitySold`
- `UnitPriceSold`
- `Discount`

### Purchase
- `Date`
- `ItemID`
- `QuantityBought`
- `UnitCost`

### Expenses
- `Month` (example: `January`)
- At least one expense column such as:
	- `Salary`, `Rent`, `Utilities`, `Marketing`, `EMI`, `Interest`, `Other`, or `Others`

## Dashboard Scope Controls

- **Period** options: `monthly`, `quarterly`, `semiannual`, `annual`
- **Bucket** options depend on selected period:
	- Monthly: `Jan` ... `Dec`
	- Quarterly: `Q1` ... `Q4`
	- Semiannual: `H1`, `H2`
	- Annual: `Year`
	- Or `all` for full period

Use **Apply Scope** to refresh analytics for selected scope.

## Backend Endpoints Used by Frontend

### Analysis
- `/analysis/profitability`
- `/analysis/discounts`
- `/analysis/inventory`
- `/analysis/products`
- `/analysis/expenses`
- `/analysis/monthly-growth`
- `/analysis/breakeven`
- `/analysis/cashflow`

### Reports
- `/report/pdf`
- `/report/excel`

All requests include `period`, and include `bucket` when bucket is not `all`.

## API Base URL Setting

In the dashboard sidebar, set **API Base URL** to your backend origin.

Default:

```text
http://127.0.0.1:8002
```

The value is saved in localStorage key `dashboard_api_base`.

## Common Issues and Fixes

### Upload fails
- Confirm file extension is `.xlsx` or `.xls`.
- Confirm all 4 required sheets exist with correct names.

### Dashboard loads but cards/charts are empty
- Ensure backend is running on the configured API Base URL.
- Upload at least one valid workbook first.
- Click **Apply Scope** again.
- Try `period=monthly` and `bucket=all`.

### Some sections render, others fail
- Frontend is designed for partial rendering.
- Check error panel for failed endpoint names/status.
- Verify backend data supports requested scope.

### Backend says no data loaded
- Upload file via `/docs` using `POST /upload`, or
- Place Excel in backend `data/raw` and restart backend for bootstrap load.

### Scope returns no data
- Backend returns 400 when selected bucket has no rows.
- Select a different bucket or use `all`.

## Daily Operating Steps

1. Start services with `start_frontend_backend.bat`.
2. Upload latest Excel workbook from backend docs (`POST /upload`).
3. Open dashboard and verify API Base URL.
4. Select period and bucket, then apply scope.
5. Review KPIs/charts/tables.
6. Download PDF or Excel report as needed.

## Notes for Developers

- Frontend is static and framework-free.
- Uses browser `fetch` and ApexCharts.
- Calls analysis endpoints concurrently.
- Backend CORS is permissive for local multi-port setup.
