"""
analysis/expenses.py  -  Section 6: Expense Analysis
"""
from logger import get_logger
logger = get_logger(__name__)

EXP_COLS = ["Salary", "Rent", "Utilities", "Marketing", "EMI", "Interest", "Other"]


def compute_expenses(store: dict) -> dict:
    exp = store["exp"]
    v   = store["vars"]

    OpExPctRevenue = (v["TotalOperatingExpense"] / v["TotalRevenue"]) * 100
    breakdown      = {col: round(float(exp[col].sum()), 2) for col in EXP_COLS if col in exp.columns}

    exp2 = exp.copy()
    exp2["TotalExpense"] = exp2[[c for c in EXP_COLS if c in exp2.columns]].sum(axis=1)
    monthly = exp2[["Month", "TotalExpense"]].to_dict(orient="records")

    logger.info(f"Expenses: OpEx%={OpExPctRevenue:.2f}")
    return {
        "total_opex_npr":       round(v["TotalOperatingExpense"], 2),
        "opex_pct_of_revenue":  round(OpExPctRevenue, 2),
        "expense_breakdown":    breakdown,
        "monthly_expenses":     monthly,
    }
