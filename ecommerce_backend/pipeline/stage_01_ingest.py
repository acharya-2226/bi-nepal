"""
stage_01_ingest.py  -  Load all 4 sheets from the uploaded Excel file.
"""
from pathlib import Path
import pandas as pd
from logger import get_logger

logger = get_logger(__name__)


def ingest(context: dict) -> dict:
    path = Path(context["file_path"])
    logger.info(f"Ingesting: {path.name}")

    inv   = pd.read_excel(path, sheet_name="Inventory")
    sales = pd.read_excel(path, sheet_name="Sales")
    purch = pd.read_excel(path, sheet_name="Purchase")
    exp   = pd.read_excel(path, sheet_name="Expenses")

    logger.info(f"Loaded  Inventory:{len(inv)}  Sales:{len(sales)}  Purchase:{len(purch)}  Expenses:{len(exp)}")
    context.update({"inv": inv, "sales": sales, "purch": purch, "exp": exp})
    return context
