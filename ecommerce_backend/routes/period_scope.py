"""
routes/period_scope.py  -  Build month-scoped store slices from period/bucket inputs.
"""

from fastapi import HTTPException

from analysis.period_utils import normalize_period
from pipeline.stage_03_transform import transform

MONTH_BUCKETS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def bucket_options(period: str) -> list[str]:
    period = normalize_period(period)
    if period == "monthly":
        return MONTH_BUCKETS
    if period == "quarterly":
        return ["Q1", "Q2", "Q3", "Q4"]
    if period == "semiannual":
        return ["H1", "H2"]
    return ["Year"]


def selected_labels(period: str, bucket: str | None) -> list[str]:
    labels = bucket_options(period)
    if not bucket or bucket.lower() == "all":
        return labels
    if bucket in labels:
        return [bucket]
    return []


def bucket_months(period: str, bucket: str | None) -> set[int]:
    period = normalize_period(period)
    if not bucket or bucket.lower() == "all":
        return set(range(1, 13))

    b = bucket.strip()
    allowed = bucket_options(period)
    if b not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid bucket '{bucket}' for period '{period}'. Allowed: {', '.join(allowed)}",
        )

    if period == "monthly":
        return {MONTH_BUCKETS.index(b) + 1}
    if period == "quarterly":
        q = int(b[1])
        start = (q - 1) * 3 + 1
        return {start, start + 1, start + 2}
    if period == "semiannual":
        return set(range(1, 7)) if b == "H1" else set(range(7, 13))
    return set(range(1, 13))


def _map_exp_month_to_num(exp_df):
    month_map = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    df = exp_df.copy()
    df["MonthNum"] = df["Month"].map(month_map)
    return df


def scoped_store(store: dict, period: str, bucket: str | None) -> dict:
    months = bucket_months(period, bucket)

    sales = store["sales"]
    purch = store["purch"]
    exp = store["exp"]
    inv = store["inv"]

    sales_f = sales[sales["MonthNum"].isin(months)].copy()
    purch_f = purch[purch["Month"].isin(months)].copy()
    exp_f = _map_exp_month_to_num(exp)
    exp_f = exp_f[exp_f["MonthNum"].isin(months)].drop(columns=["MonthNum"])

    if sales_f.empty or purch_f.empty or exp_f.empty:
        raise HTTPException(
            status_code=400,
            detail="No data available for the selected period bucket.",
        )

    scoped = {
        "inv": inv.copy(),
        "sales": sales_f,
        "purch": purch_f,
        "exp": exp_f,
    }
    scoped = transform(scoped)
    scoped["ready"] = True
    return scoped
