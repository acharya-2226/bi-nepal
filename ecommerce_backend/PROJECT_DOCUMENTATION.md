# 📊 Small Business Analysis API - Executive Summary

---

## 🎯 Purpose [Problem Statement]

This backend provides **business intelligence for small ecommerce operations**.  
It accepts Excel uploads, cleans and transforms the data, stores it in SQLite, serves analytics through FastAPI endpoints, and exports PDF/Excel reports.

---

## 🚀 What It Delivers

- 📥 Unified upload-to-analysis workflow  
- 🧹 Automated data cleaning and metric preparation  
- 🗄️ Persistent storage with deduplication  
- 🌐 JSON analysis endpoints for dashboard consumption  
- 📄 Downloadable BI reports in **PDF & Excel** formats  

---

## 🔄 Core Workflow

1. 📤 User uploads an Excel workbook *(Inventory, Sales, Purchase, Expenses)*  
2. ⚙️ A **3-stage pipeline** runs:
   - 📥 **Ingest** → Read sheets into DataFrames  
   - 🧹 **Clean** → Normalize columns, parse dates, handle missing values, remove invalid/duplicate rows  
   - 🔧 **Transform** → Compute aggregates *(revenue, discounts, COGS, expenses, quantities)*  
3. 🗄️ Processed data is merged into SQLite tables  
4. ⚡ In-memory runtime state is refreshed for fast API access  

---

## 🧠 Runtime Design

- 🗄️ SQLite → **Source of Truth**  
- ⚡ In-memory store → **Cache layer for APIs**  
- 🔁 Startup behavior:
  - Load from SQLite  
  - If empty → Bootstrap from `data/raw`  

---

## 🌐 Main API Surface

- 📥 Upload → `POST /upload`  
- 📊 Analysis:
  - `/analysis/profitability`  
  - `/analysis/discounts`  
  - `/analysis/inventory`  
  - `/analysis/products`  
  - `/analysis/expenses`  
  - `/analysis/monthly-growth`  
  - `/analysis/breakeven`  
  - `/analysis/cashflow`  

- 📄 Reports:
  - `/report/pdf`  
  - `/report/excel`  

- 📘 API Docs:
  - `/docs`  
  - `/redoc`  

---

## 🖥️ Frontend Integration (Static Dashboard)

- 📁 Frontend location:  
  [`ecommerce_frontend/static_dashboard`](../ecommerce_frontend/static_dashboard)

- 🌐 Direct API calls via JavaScript (`fetch`)  

- 🎛️ Features:
  - API base URL configuration  
  - Period & bucket filtering  
  - KPI cards, tables, charts  
  - Report export buttons  

- 📄 Report triggers:
  - `/report/pdf`  
  - `/report/excel`  

---

## 📊 Reports Generated

- 📄 **PDF Report**
  - Profitability  
  - Cash Flow  
  - Inventory  
  - Break-even  

- 📊 **Excel Report**
  - Profitability  
  - Growth  
  - Products  
  - Expenses  
  - Cash Flow  
  - Break-even  
  - Reorder alerts  

---

## 🛠️ Tech Stack

- 🐍 Python 3.12  
- ⚡ FastAPI + Uvicorn  
- 🐼 pandas + numpy  
- 🗄️ sqlite3  
- 📊 openpyxl (Excel I/O)  
- 📄 reportlab (PDF export)  
- 📈 matplotlib (visual assets)  
- 📦 fpdf2 *(legacy dependency)*  

---

## ⚠️ Current Constraints

- ❌ No formal schema migrations  
- ⚠️ Full-row deduplication only *(no business-key logic)*  
- ⚠️ Implicit column validation  
- ⚠️ Single-process cache model  

---

## 🚀 Recommended Next Steps

1. ✅ Add strict schema validation per sheet  
2. 🔄 Introduce DB migration/versioning  
3. 🧠 Implement business-key dedupe/upsert  
4. 🧪 Add automated tests (pipeline + APIs)  
5. 🔐 Add authentication for production use  

---

## ▶️ Run Quickstart

1. 📦 Install dependencies:
   ```bash
   pip install -r ecommerce_backend/requirements.txt
   ## ▶️ Run Quickstart ### 🚀 Start API
bash
cd ecommerce_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8002
🌐 Open API Docs

http://127.0.0.1:8002/docs

⚡ Combined Launcher (Backend + Frontend)
▶️ Run
start_frontend_backend.bat
🔗 Services Started
Backend → http://127.0.0.1:8002
Frontend → http://127.0.0.1:8010
