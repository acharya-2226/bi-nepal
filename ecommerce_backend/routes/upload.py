"""
routes/upload.py  -  POST /upload
Saves the Excel file, runs the full pipeline, populates state.
"""
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from logger import get_logger
from pipeline.runner import run_pipeline
import state
from database import merge_context, load_store

router = APIRouter()
logger = get_logger(__name__)

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx / .xls) are supported.")

    dest = UPLOAD_DIR / file.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    logger.info(f"File saved: {dest}")

    try:
        context = run_pipeline(str(dest))
    except Exception as exc:
        logger.exception("Pipeline failed.")
        raise HTTPException(status_code=500, detail=f"Pipeline error: {exc}")

    merge_context(context, source_filename=file.filename)
    state.store.update(load_store())
    logger.info("State updated. Ready for analysis requests.")
    return {"message": "Upload successful. Data merged into SQLite.", "file": file.filename}
