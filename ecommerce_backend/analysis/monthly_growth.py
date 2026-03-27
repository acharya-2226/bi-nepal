"""
analysis/monthly_growth.py  -  Section 7: Period Growth Metrics
"""
from logger import get_logger
from analysis.period_utils import normalize_period, period_labels, aggregate_month_values, growth_pct

logger = get_logger(__name__)

EXP_COLS    = ["Salary", "Rent", "Utilities", "Marketing", "EMI", "Interest", "Other"]
MONTH_NAMES = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]


def compute_monthly_growth(store: dict, period: str = "monthly") -> dict:
    period = normalize_period(period)
    sales = store["sales"]
    exp   = store["exp"]
    v     = store["vars"]

    monthly_rev_map = (
        sales.groupby("MonthNum")
        .apply(lambda d: (d["QuantitySold"] * d["UnitPriceSold"]).sum() - d["Discount"].sum())
        .to_dict()
    )

    exp2 = exp.copy()
    exp2["MonthNum"]     = exp2["Month"].map({m: i+1 for i, m in enumerate(MONTH_NAMES)})
    exp2["TotalExpense"] = exp2[[c for c in EXP_COLS if c in exp2.columns]].sum(axis=1)
    monthly_exp_map = exp2.groupby("MonthNum")["TotalExpense"].sum().to_dict()

    revenue_series = aggregate_month_values(monthly_rev_map, period)

    total_revenue = float(v.get("TotalRevenue", 0) or 0)
    if total_revenue > 0:
        month_cogs_map = {
            month: (float(revenue or 0) / total_revenue) * float(v.get("COGS", 0) or 0)
            for month, revenue in monthly_rev_map.items()
        }
    else:
        month_cogs_map = {month: 0.0 for month in range(1, 13)}

    cogs_series = aggregate_month_values(month_cogs_map, period)
    expense_series = aggregate_month_values(monthly_exp_map, period)
    profit_series = [
        revenue_series[idx] - cogs_series[idx] - expense_series[idx]
        for idx in range(len(revenue_series))
    ]
    rev_growth = growth_pct(revenue_series)
    prof_growth = growth_pct(profit_series)

    labels = period_labels(period)
    rows = []
    for idx, label in enumerate(labels):
        rows.append(
            {
                "PeriodIndex": idx + 1,
                "PeriodLabel": label,
                "MonthRevenue": round(revenue_series[idx], 2),
                "MonthProfit": round(profit_series[idx], 2),
                "RevGrowth": round(rev_growth[idx], 2) if rev_growth[idx] is not None else None,
                "ProfGrowth": round(prof_growth[idx], 2) if prof_growth[idx] is not None else None,
            }
        )

    logger.info(f"{period.title()} growth computed.")
    return {
        "period": period,
        "monthly": rows,
    }
