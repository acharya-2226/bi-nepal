"""
stage_02_clean.py  -  Parse dates, add time columns, and clean missing values.
"""
import pandas as pd
from logger import get_logger

logger = get_logger(__name__)


def _strip_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    return df


def _strip_text_fields(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def _to_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _series_mode(series: pd.Series):
    non_null = series.dropna()
    if non_null.empty:
        return None
    modes = non_null.mode(dropna=True)
    if modes.empty:
        return non_null.iloc[0]
    return modes.iloc[0]


def _series_median(series: pd.Series):
    non_null = series.dropna()
    if non_null.empty:
        return None
    return non_null.median()


def _fill_with_mode(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col not in df.columns:
        return df
    mode_val = _series_mode(df[col])
    if mode_val is not None:
        df[col] = df[col].fillna(mode_val)
    return df


def _fill_with_median(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col not in df.columns:
        return df
    median_val = _series_median(df[col])
    if median_val is not None:
        df[col] = df[col].fillna(median_val)
    return df


def clean(context: dict) -> dict:
    inv = _strip_columns(context["inv"])
    sales = _strip_columns(context["sales"])
    purch = _strip_columns(context["purch"])
    exp = _strip_columns(context["exp"])

    # Keep legacy normalization.
    if "Others" in exp.columns and "Other" not in exp.columns:
        exp.rename(columns={"Others": "Other"}, inplace=True)

    # Trim string fields from the notebook process.
    inv = _strip_text_fields(inv, ["ItemID", "ItemName"])
    sales = _strip_text_fields(sales, ["ItemID", "DeliveryType", "PaymentMode"])
    purch = _strip_text_fields(purch, ["ItemID", "PaymentType"])

    # Parse dates.
    if "Date" in sales.columns:
        sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
    if "Date" in purch.columns:
        purch["Date"] = pd.to_datetime(purch["Date"], errors="coerce")

    # Numeric coercion.
    inv = _to_numeric(inv, ["OpeningStock", "CostPrice", "SellingPrice", "ReorderLevel"])
    sales = _to_numeric(sales, ["QuantitySold", "UnitPriceSold", "DeliveryCharge", "Discount"])
    purch = _to_numeric(purch, ["QuantityBought", "UnitCost", "TransportCost"])
    exp = _to_numeric(exp, ["Salary", "Rent", "Utilities", "Marketing", "EMI", "Interest", "Other"])

    # Inventory missing-value rules.
    if "ItemName" in inv.columns:
        inv["ItemName"] = inv["ItemName"].replace(r"^\s*$", pd.NA, regex=True)
        inv = inv[inv["ItemName"].notna()]
    if "Category" in inv.columns:
        inv["Category"] = inv["Category"].replace(r"^\s*$", pd.NA, regex=True)
    inv = _fill_with_mode(inv, "Category")
    inv = _fill_with_median(inv, "OpeningStock")
    inv = _fill_with_median(inv, "CostPrice")
    inv = _fill_with_median(inv, "SellingPrice")
    inv = _fill_with_median(inv, "ReorderLevel")

    # Sales missing-value rules.
    sales = _fill_with_median(sales, "QuantitySold")
    sales = _fill_with_median(sales, "UnitPriceSold")
    if "DeliveryType" in sales.columns:
        sales["DeliveryType"] = sales["DeliveryType"].replace(r"^\s*$", pd.NA, regex=True)
    sales = _fill_with_mode(sales, "DeliveryType")
    if "DeliveryCharge" in sales.columns:
        if "DeliveryType" in sales.columns:
            pickup_mask = sales["DeliveryType"].eq("Pickup")
            pickup_median = _series_median(sales.loc[pickup_mask, "DeliveryCharge"])
            non_pickup_median = _series_median(sales.loc[~pickup_mask, "DeliveryCharge"])
            overall_median = _series_median(sales["DeliveryCharge"])

            if pickup_median is not None:
                sales.loc[pickup_mask, "DeliveryCharge"] = sales.loc[pickup_mask, "DeliveryCharge"].fillna(pickup_median)
            elif overall_median is not None:
                sales.loc[pickup_mask, "DeliveryCharge"] = sales.loc[pickup_mask, "DeliveryCharge"].fillna(overall_median)

            if non_pickup_median is not None:
                sales.loc[~pickup_mask, "DeliveryCharge"] = sales.loc[~pickup_mask, "DeliveryCharge"].fillna(
                    non_pickup_median
                )
            elif overall_median is not None:
                sales.loc[~pickup_mask, "DeliveryCharge"] = sales.loc[~pickup_mask, "DeliveryCharge"].fillna(
                    overall_median
                )
        else:
            sales = _fill_with_median(sales, "DeliveryCharge")
    sales = _fill_with_median(sales, "Discount")
    if "PaymentMode" in sales.columns:
        sales["PaymentMode"] = sales["PaymentMode"].replace(r"^\s*$", pd.NA, regex=True)
    sales = _fill_with_mode(sales, "PaymentMode")

    # Purchase missing-value rules.
    purch = _fill_with_median(purch, "QuantityBought")
    purch = _fill_with_median(purch, "UnitCost")
    purch = _fill_with_median(purch, "TransportCost")
    if "PaymentType" in purch.columns:
        purch["PaymentType"] = purch["PaymentType"].replace(r"^\s*$", pd.NA, regex=True)
    purch = _fill_with_mode(purch, "PaymentType")

    # Expenses missing-value rules.
    exp = _fill_with_median(exp, "Salary")
    exp = _fill_with_median(exp, "Rent")
    exp = _fill_with_median(exp, "Utilities")
    exp = _fill_with_median(exp, "Marketing")
    exp = _fill_with_median(exp, "EMI")
    exp = _fill_with_median(exp, "Interest")
    exp = _fill_with_median(exp, "Other")

    # Remove duplicate rows (notebook behavior).
    before_inv, before_sales, before_purch = len(inv), len(sales), len(purch)
    inv = inv.drop_duplicates()
    sales = sales.drop_duplicates()
    purch = purch.drop_duplicates()

    # Remove invalid transactional values (notebook behavior).
    if "QuantitySold" in sales.columns:
        sales = sales[sales["QuantitySold"] > 0]
    if "QuantityBought" in purch.columns:
        purch = purch[purch["QuantityBought"] > 0]
    if "UnitPriceSold" in sales.columns:
        sales = sales[sales["UnitPriceSold"] >= 0]
    if "UnitCost" in purch.columns:
        purch = purch[purch["UnitCost"] >= 0]

    # Remove fully empty rows.
    for label, df in [("sales", sales), ("purch", purch)]:
        before = len(df)
        df.dropna(how="all", inplace=True)
        logger.info(f"Cleaned {label}: removed {before - len(df)} fully-empty rows")

    # Sort by date (notebook behavior).
    if "Date" in sales.columns:
        sales = sales.sort_values(by="Date")
    if "Date" in purch.columns:
        purch = purch.sort_values(by="Date")

    # Time fields used by analysis modules.
    if "Date" in sales.columns:
        sales["Month"] = sales["Date"].dt.month
        sales["Year"] = sales["Date"].dt.year
        sales["MonthName"] = sales["Date"].dt.strftime("%b")
        sales["MonthNum"] = sales["Date"].dt.month
    if "Date" in purch.columns:
        purch["Month"] = purch["Date"].dt.month
        purch["Year"] = purch["Date"].dt.year

    logger.info(
        "Clean summary: inv -%d dup, sales -%d dup, purch -%d dup",
        before_inv - len(inv),
        before_sales - len(sales),
        before_purch - len(purch),
    )

    context.update({"inv": inv, "sales": sales, "purch": purch, "exp": exp})
    return context
