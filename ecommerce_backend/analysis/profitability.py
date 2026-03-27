"""
analysis/profitability.py  -  Section 2: Profitability Metrics
"""
from logger import get_logger
logger = get_logger(__name__)


def _pct(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return (numerator / denominator) * 100


def compute_profitability(store: dict) -> dict:
    v = store.get("vars") or {}

    gross_revenue = float(v.get("GrossRevenue", 0))
    total_discount = float(v.get("TotalDiscount", 0))
    total_revenue = float(v.get("TotalRevenue", 0))
    cogs = float(v.get("COGS", 0))
    total_opex = float(v.get("TotalOperatingExpense", 0))

    GrossProfit = total_revenue - cogs
    GrossProfitMargin = _pct(GrossProfit, total_revenue)
    NetProfit = GrossProfit - total_opex
    NetProfitMargin = _pct(NetProfit, total_revenue)

    logger.info(f"Profitability: NetProfit={NetProfit:,.0f}  GPM={GrossProfitMargin:.2f}%")
    return {
        "gross_revenue_npr":       round(gross_revenue, 2),
        "total_discount_npr":      round(total_discount, 2),
        "net_revenue_npr":         round(total_revenue, 2),
        "cogs_npr":                round(cogs, 2),
        "gross_profit_npr":        round(GrossProfit, 2),
        "gross_profit_margin_pct": round(GrossProfitMargin, 2),
        "total_opex_npr":          round(total_opex, 2),
        "net_profit_npr":          round(NetProfit, 2),
        "net_profit_margin_pct":   round(NetProfitMargin, 2),
    }
