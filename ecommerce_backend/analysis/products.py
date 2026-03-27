"""
analysis/products.py  -  Section 5: Product-Level Metrics
"""
from logger import get_logger
logger = get_logger(__name__)


def compute_products(store: dict) -> dict:
    inv   = store["inv"]
    sales = store["sales"]
    v     = store["vars"]

    prod = inv[["ItemID", "ItemName", "Category", "SellingPrice"]].set_index("ItemID").copy()
    prod_rev  = sales.groupby("ItemID").apply(lambda d: (d["QuantitySold"] * d["UnitPriceSold"]).sum()).rename("GrossRev")
    prod_disc = sales.groupby("ItemID")["Discount"].sum().rename("Disc")
    prod_qty  = sales.groupby("ItemID")["QuantitySold"].sum().rename("QtySold")

    prod = prod.join(prod_rev).join(prod_disc).join(prod_qty)
    prod["ProductRevenue"] = prod["GrossRev"].fillna(0) - prod["Disc"].fillna(0)
    prod["ProductQtySold"] = prod["QtySold"].fillna(0)
    prod["ProductProfit"]  = prod["ProductRevenue"] - prod["ProductQtySold"] * v["WeightedAvgCost"]
    prod["ContribPct"]     = (prod["ProductRevenue"] / v["TotalRevenue"]) * 100

    top10 = (
        prod.sort_values("ProductRevenue", ascending=False).head(10)
            [["ItemName", "Category", "ProductQtySold", "ProductRevenue", "ProductProfit", "ContribPct"]]
            .round(2).reset_index().to_dict(orient="records")
    )
    by_cat = (
        prod.groupby("Category")["ProductRevenue"].sum()
            .sort_values(ascending=False).reset_index()
            .rename(columns={"ProductRevenue": "category_revenue_npr"})
            .to_dict(orient="records")
    )

    logger.info("Product metrics computed.")
    return {"top_10_products_by_revenue": top10, "revenue_by_category": by_cat}
