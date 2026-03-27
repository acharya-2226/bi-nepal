"""
analysis/inventory.py  -  Section 4: Inventory Metrics
"""
from logger import get_logger
logger = get_logger(__name__)


def compute_inventory(store: dict) -> dict:
    inv   = store["inv"]
    sales = store["sales"]
    v     = store["vars"]

    InventoryTurnover        = v["COGS"] / v["TotalPurchaseCost"]
    DaysInventoryOutstanding = 365 / InventoryTurnover

    qty_sold   = sales.groupby("ItemID")["QuantitySold"].sum().reset_index()
    inv_detail = inv.merge(qty_sold, on="ItemID", how="left")
    inv_detail["QuantitySold"] = inv_detail["QuantitySold"].fillna(0)
    inv_detail["ClosingStock"] = inv_detail["OpeningStock"] - inv_detail["QuantitySold"]
    below = inv_detail[inv_detail["ClosingStock"] < inv_detail["ReorderLevel"]]

    logger.info(f"Inventory: turnover={InventoryTurnover:.2f}x  DIO={DaysInventoryOutstanding:.1f}d")
    return {
        "inventory_turnover":          round(InventoryTurnover, 2),
        "days_inventory_outstanding":  round(DaysInventoryOutstanding, 1),
        "items_below_reorder_level":   len(below),
        "below_reorder_items": below[["ItemID", "ItemName", "ClosingStock", "ReorderLevel"]].to_dict(orient="records"),
    }
