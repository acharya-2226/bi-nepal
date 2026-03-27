"""
analysis/period_utils.py  -  Reusable monthly/quarterly/semiannual/annual helpers.
"""

from collections.abc import Iterable

MONTH_LABELS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def normalize_period(period: str | None) -> str:
    normalized = (period or "monthly").strip().lower()
    if normalized in {"monthly", "quarterly", "semiannual", "annual"}:
        return normalized
    return "monthly"


def period_labels(period: str) -> list[str]:
    period = normalize_period(period)
    if period == "monthly":
        return MONTH_LABELS.copy()
    if period == "quarterly":
        return ["Q1", "Q2", "Q3", "Q4"]
    if period == "semiannual":
        return ["H1", "H2"]
    return ["Year"]


def month_to_bucket(month_num: int, period: str) -> int:
    period = normalize_period(period)
    month_num = max(1, min(12, int(month_num)))
    if period == "monthly":
        return month_num
    if period == "quarterly":
        return ((month_num - 1) // 3) + 1
    if period == "semiannual":
        return 1 if month_num <= 6 else 2
    return 1


def aggregate_month_values(values_by_month: dict[int, float], period: str) -> list[float]:
    labels = period_labels(period)
    totals = [0.0 for _ in labels]
    for month_num in range(1, 13):
        bucket = month_to_bucket(month_num, period)
        totals[bucket - 1] += float(values_by_month.get(month_num, 0.0) or 0.0)
    return totals


def growth_pct(series: Iterable[float]) -> list[float | None]:
    values = list(series)
    out: list[float | None] = []
    prev = None
    for val in values:
        if prev in (None, 0):
            out.append(None)
        else:
            out.append(((val - prev) / prev) * 100)
        prev = val
    return out
