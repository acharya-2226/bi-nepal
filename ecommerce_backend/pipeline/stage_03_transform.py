"""
stage_03_transform.py  -  Compute core derived variables (Section 1 of notebook).
Results stored in context["vars"] and used by all analysis modules.
"""
from logger import get_logger

logger = get_logger(__name__)

EXP_COLS = ["Salary", "Rent", "Utilities", "Marketing", "EMI", "Interest", "Other"]


def transform(context: dict) -> dict:
    sales = context["sales"]
    purch = context["purch"]
    exp   = context["exp"]

    TotalQuantitySold    = sales["QuantitySold"].sum()
    TotalQuantityBought  = purch["QuantityBought"].sum()
    GrossRevenue         = (sales["QuantitySold"] * sales["UnitPriceSold"]).sum()
    TotalDiscount        = sales["Discount"].sum()
    TotalRevenue         = GrossRevenue - TotalDiscount
    TotalPurchaseCost    = (purch["QuantityBought"] * purch["UnitCost"]).sum()
    WeightedAvgCost      = (TotalPurchaseCost / TotalQuantityBought) if TotalQuantityBought else 0
    COGS                 = TotalQuantitySold * WeightedAvgCost
    TotalOperatingExpense = exp[[c for c in EXP_COLS if c in exp.columns]].sum().sum()

    context["vars"] = {
        "TotalQuantitySold":     TotalQuantitySold,
        "TotalQuantityBought":   TotalQuantityBought,
        "GrossRevenue":          GrossRevenue,
        "TotalDiscount":         TotalDiscount,
        "TotalRevenue":          TotalRevenue,
        "TotalPurchaseCost":     TotalPurchaseCost,
        "WeightedAvgCost":       WeightedAvgCost,
        "COGS":                  COGS,
        "TotalOperatingExpense": TotalOperatingExpense,
    }

    logger.info(f"Transform done. GrossRevenue={GrossRevenue:,.0f}  NetRevenue={TotalRevenue:,.0f}")
    return context
