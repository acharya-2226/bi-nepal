"""
routes/report.py  -  GET /report/pdf  and  GET /report/excel
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from logger import get_logger
from reports.report_generator import generate_pdf, generate_excel
from routes.period_scope import scoped_store
import state

router = APIRouter(prefix="/report")
logger = get_logger(__name__)


def _require_data():
    if not state.store["ready"]:
        raise HTTPException(
            status_code=400,
            detail="No data loaded. Upload a file or place an Excel file in data/raw and restart.",
        )


@router.get("/pdf")
def download_pdf(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    path = generate_pdf(store, period=period, bucket=bucket)
    response = FileResponse(
        path,
        media_type="application/pdf",
        filename=f"BI_Report_{period}_{(bucket or 'all').replace(' ', '')}.pdf",
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


@router.get("/excel")
def download_excel(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    path = generate_excel(store, period=period, bucket=bucket)
    response = FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"BI_Report_{period}_{(bucket or 'all').replace(' ', '')}.xlsx",
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response
