"""
routes/analysis.py  -  One GET endpoint per BI section.
"""
from fastapi import APIRouter, HTTPException
from logger import get_logger
import state

from analysis.profitability  import compute_profitability
from analysis.discounts      import compute_discounts
from analysis.inventory      import compute_inventory
from analysis.products       import compute_products
from analysis.expenses       import compute_expenses
from analysis.monthly_growth import compute_monthly_growth
from analysis.breakeven      import compute_breakeven
from analysis.cashflow       import compute_cashflow
from routes.period_scope import scoped_store, selected_labels

router = APIRouter(prefix="/analysis")
logger = get_logger(__name__)


def _require_data():
    if not state.store["ready"]:
        raise HTTPException(
            status_code=400,
            detail="No data loaded. Upload a file or place an Excel file in data/raw and restart.",
        )


@router.get("/profitability")
def profitability(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    return compute_profitability(store)


@router.get("/discounts")
def discounts(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    return compute_discounts(store)


@router.get("/inventory")
def inventory(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    return compute_inventory(store)


@router.get("/products")
def products(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    return compute_products(store)


@router.get("/expenses")
def expenses(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    return compute_expenses(store)


@router.get("/monthly-growth")
def monthly_growth(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    result = compute_monthly_growth(store, period=period)
    labels = set(selected_labels(period, bucket))
    result["monthly"] = [row for row in result.get("monthly", []) if row.get("PeriodLabel") in labels]
    return result


@router.get("/breakeven")
def breakeven(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    return compute_breakeven(store)


@router.get("/cashflow")
def cashflow(period: str = "monthly", bucket: str | None = None):
    _require_data()
    store = scoped_store(state.store, period=period, bucket=bucket)
    result = compute_cashflow(store, period=period)
    labels = set(selected_labels(period, bucket))
    result["monthly_cashflow"] = [
        row for row in result.get("monthly_cashflow", []) if row.get("PeriodLabel") in labels
    ]
    return result
