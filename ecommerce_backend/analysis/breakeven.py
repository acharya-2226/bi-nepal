"""
analysis/breakeven.py  -  Section 8: Break-Even Analysis
"""
from logger import get_logger
logger = get_logger(__name__)


def compute_breakeven(store: dict) -> dict:
    inv = store["inv"]
    v   = store["vars"]

    be = inv[["ItemID", "ItemName", "Category", "SellingPrice"]].copy()
    be["ContribPerUnit"] = (be["SellingPrice"] - v["WeightedAvgCost"]).clip(lower=0.01)
    be["BreakEvenUnits"] = v["TotalOperatingExpense"] / be["ContribPerUnit"]

    avg_contrib      = float(be["ContribPerUnit"].mean())
    overall_beu      = v["TotalOperatingExpense"] / avg_contrib
    margin_of_safety = ((v["TotalQuantitySold"] - overall_beu) / v["TotalQuantitySold"]) * 100

    top20 = (
        be[be["BreakEvenUnits"] < 1e6].sort_values("BreakEvenUnits").head(20)
          [["ItemID", "ItemName", "BreakEvenUnits", "ContribPerUnit"]].round(2).to_dict(orient="records")
    )

    logger.info(f"Break-even: BEU={overall_beu:,.0f}  MoS={margin_of_safety:.2f}%")
    return {
        "weighted_avg_cost_npr":    round(v["WeightedAvgCost"], 2),
        "avg_contrib_per_unit_npr": round(avg_contrib, 2),
        "total_opex_npr":           round(v["TotalOperatingExpense"], 2),
        "overall_breakeven_units":  round(overall_beu, 0),
        "actual_units_sold":        int(v["TotalQuantitySold"]),
        "margin_of_safety_pct":     round(margin_of_safety, 2),
        "top_20_easiest_breakeven": top20,
    }
