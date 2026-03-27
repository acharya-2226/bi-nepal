"""
analysis/cashflow.py  -  Section 9: Cash Flow
"""
from logger import get_logger
from analysis.period_utils import normalize_period, period_labels, aggregate_month_values

logger = get_logger(__name__)


def compute_cashflow(store: dict, period: str = "monthly") -> dict:
    period = normalize_period(period)
    sales = store["sales"]
    purch = store["purch"]
    v     = store["vars"]

    TotalCashInflow  = v["TotalRevenue"]
    TotalCashOutflow = v["TotalPurchaseCost"] + v["TotalOperatingExpense"]
    NetCashMovement  = TotalCashInflow - TotalCashOutflow

    monthly_in_map  = sales.groupby("MonthNum").apply(
        lambda d: (d["QuantitySold"] * d["UnitPriceSold"]).sum() - d["Discount"].sum()
    ).to_dict()

    monthly_out_map = purch.groupby("Month").apply(
        lambda d: (d["QuantityBought"] * d["UnitCost"]).sum()
    ).to_dict()

    cash_in_series = aggregate_month_values(monthly_in_map, period)
    cash_out_series = aggregate_month_values(monthly_out_map, period)
    labels = period_labels(period)

    monthly_cf = []
    for idx, label in enumerate(labels):
        cash_in = round(cash_in_series[idx], 2)
        cash_out = round(cash_out_series[idx], 2)
        monthly_cf.append(
            {
                "PeriodIndex": idx + 1,
                "PeriodLabel": label,
                "CashIn": cash_in,
                "CashOut": cash_out,
                "NetCash": round(cash_in - cash_out, 2),
            }
        )

    logger.info(f"{period.title()} cashflow: NetCashMovement={NetCashMovement:,.0f}")
    return {
        "period": period,
        "total_cash_inflow_npr":  round(TotalCashInflow, 2),
        "total_cash_outflow_npr": round(TotalCashOutflow, 2),
        "net_cash_movement_npr":  round(NetCashMovement, 2),
        "monthly_cashflow": monthly_cf,
    }
