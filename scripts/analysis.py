# scripts/analysis.py
import pandas as pd
from db_connect import load_data
import os

# Ensure outputs folder exists
os.makedirs("outputs", exist_ok=True)

df = load_data("orders")
df["Order Date"] = pd.to_datetime(df["Order Date"])

# ==== KPI Tables / Summaries ====
def top_products(n=10):
    result = df.groupby("Product Name")["Sales"].sum().nlargest(n).reset_index()
    result.to_csv("outputs/top_products.csv", index=False)
    return result

def top_customers(n=10):
    result = df.groupby("Customer Name")["Sales"].sum().nlargest(n).reset_index()
    result.to_csv("outputs/top_customers.csv", index=False)
    return result

def sales_by_category():
    result = df.groupby("Category")["Sales"].sum().reset_index()
    result.to_csv("outputs/sales_by_category.csv", index=False)
    return result

def monthly_sales_trend():
    result = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
    result["Order Date"] = result["Order Date"].astype(str)
    result.to_csv("outputs/monthly_sales_trend.csv", index=False)
    return result

# Run all analyses
if __name__ == "__main__":
    print("📊 Running structured analysis...")
    top_products()
    top_customers()
    sales_by_category()
    monthly_sales_trend()
    print("✅ Analysis outputs saved in outputs/")
