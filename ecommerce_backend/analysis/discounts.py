"""
analysis/discounts.py  -  Section 3: Discount Metrics
"""
from logger import get_logger
logger = get_logger(__name__)


def compute_discounts(store: dict) -> dict:
    sales = store["sales"]
    v     = store["vars"]

    DiscountPercent   = (v["TotalDiscount"] / v["GrossRevenue"]) * 100
    DiscountedTxns    = int((sales["Discount"] > 0).sum())
    TotalTxns         = len(sales)
    DiscountedTxnPct  = (DiscountedTxns / TotalTxns) * 100
    AvgDiscPerTxn     = float(sales.loc[sales["Discount"] > 0, "Discount"].mean())

    monthly = (
        sales.groupby("MonthNum")["Discount"].sum()
             .reset_index()
             .rename(columns={"Discount": "monthly_discount_npr"})
             .to_dict(orient="records")
    )

    logger.info(f"Discounts: {DiscountPercent:.2f}% of gross revenue")
    return {
        "total_discount_npr":       round(v["TotalDiscount"], 2),
        "discount_pct_of_revenue":  round(DiscountPercent, 2),
        "discounted_transactions":  DiscountedTxns,
        "total_transactions":       TotalTxns,
        "discounted_txn_pct":       round(DiscountedTxnPct, 2),
        "avg_discount_per_txn_npr": round(AvgDiscPerTxn, 2),
        "monthly_discount":         monthly,
    }
