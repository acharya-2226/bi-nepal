"""
main.py  -  FastAPI entry point.
Run:  uvicorn main:app --reload
"""
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from logger import setup_logging, get_logger
from routes import upload, analysis, report
from pipeline.runner import run_pipeline
from database import init_db, merge_context, load_store
import state

setup_logging()
logger = get_logger(__name__)
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Nepal Ecommerce BI API",
    version="1.0.0",
    description="Upload your Excel data, then query each BI section or download a full report.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router,   tags=["Upload"])
app.include_router(analysis.router, tags=["Analysis"])
app.include_router(report.router,   tags=["Report"])


@app.on_event("startup")
async def startup():
    logger.info("Nepal Ecommerce BI API started.")
    init_db()

    # Primary path: load data already persisted in SQLite.
    store = load_store()
    if store["ready"]:
        state.store.update(store)
        logger.info("Loaded analysis data from SQLite.")
        return

    # Bootstrap path: no data in DB yet, ingest any legacy files in data/raw.
    raw_dir = BASE_DIR / "data" / "raw"
    excel_files = sorted(
        [*raw_dir.glob("*.xlsx"), *raw_dir.glob("*.xls")],
        key=lambda p: p.stat().st_mtime,
    )
    if not excel_files:
        logger.info("No SQLite data or Excel files found. Waiting for upload.")
        return

    for excel_file in excel_files:
        logger.info(f"Bootstrapping DB from: {excel_file.name}")
        context = run_pipeline(str(excel_file))
        merge_context(context, source_filename=excel_file.name)

    state.store.update(load_store())
    logger.info(f"Startup bootstrap complete. Imported {len(excel_files)} file(s) into SQLite.")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
