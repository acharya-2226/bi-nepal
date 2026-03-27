# User Guide (Static Frontend)

## Who This Is For
This guide is for business users who only need to upload files and view analytics.

## What You Need
- Windows machine
- Excel file containing these 4 sheets:
  - Inventory
  - Sales
  - Purchase
  - Expenses

## One-Time Start
1. Open the project parent folder.
2. Run `start_frontend_backend.bat`.
3. Wait for two terminal windows:
   - Backend API at `http://127.0.0.1:8002`
   - Static dashboard at `http://127.0.0.1:8010`

## Upload Your Data
1. Open `http://127.0.0.1:8002/docs`.
2. Find `POST /upload` and click **Try it out**.
3. Select your Excel file.
4. Click **Execute**.
5. Confirm response: `Upload successful. Data merged into SQLite.`

After upload, the system automatically handles cleaning, calculations, storage, and analysis updates.

## View Dashboard
1. Open `http://127.0.0.1:8010`.
2. In the left panel, confirm API Base URL is `http://127.0.0.1:8002`.
3. Choose:
  - Period: Monthly, Quarterly, Semiannual, Annual
   - Bucket: specific month/quarter/half/year or all
4. Click **Apply Scope**.

## Download Reports
Use top-right dashboard buttons:
- Download PDF Report
- Download Excel Report

Reports are generated for the selected period and bucket.

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
- at least one expense column such as:
  - `Salary`, `Rent`, `Utilities`, `Marketing`, `EMI`, `Interest`, `Other` or `Others`

## Common Issues
### Upload fails
- Ensure extension is `.xlsx` or `.xls`.
- Ensure all 4 required sheet names exist.

### Dashboard is blank or shows errors
- Confirm backend is running at `http://127.0.0.1:8002`.
- In dashboard, verify API Base URL input is correct.
- Click **Apply Scope** again.

### "No data loaded" from API
- Upload at least one valid file first using `POST /upload`.

## Daily Operating Steps
1. Run `start_frontend_backend.bat`.
2. Upload the latest Excel file from `http://127.0.0.1:8002/docs` using `POST /upload`.
3. Open dashboard and select period/bucket.
4. Review KPIs/charts/tables.
5. Download PDF/Excel reports when needed.
