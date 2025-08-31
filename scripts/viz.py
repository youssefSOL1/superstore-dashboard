# viz.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

# =========================
# 📊 Matplotlib / Seaborn Plots (static, saved as PNG)
# =========================

def plot_sales_over_time(df):
    sales_trend = df.groupby("Order Date")["Sales"].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=sales_trend, x="Order Date", y="Sales")
    plt.title("Sales Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("sales_over_time.png")
    plt.close()

def plot_sales_by_region(df):
    sales = df.groupby("Region")["Sales"].sum().reset_index()
    plt.figure(figsize=(8, 6))
    sns.barplot(data=sales, x="Region", y="Sales", palette="viridis")
    plt.title("Sales by Region")
    plt.tight_layout()
    plt.savefig("sales_by_region.png")
    plt.close()

def plot_profit_by_category(df):
    profit = df.groupby("Category")["Profit"].sum().reset_index()
    plt.figure(figsize=(8, 6))
    sns.barplot(data=profit, x="Category", y="Profit", palette="coolwarm")
    plt.title("Profit by Category")
    plt.tight_layout()
    plt.savefig("profit_by_category.png")
    plt.close()

# =========================
# 📈 Plotly Plots (interactive, used in Streamlit)
# =========================

def sales_over_time(df):
    sales_trend = df.groupby("Order Date")["Sales"].sum().reset_index()
    return px.line(
        sales_trend, x="Order Date", y="Sales",
        title="Sales Over Time"
    )

def sales_by_region(df):
    sales = df.groupby("Region")["Sales"].sum().reset_index()
    return px.bar(
        sales, x="Region", y="Sales", color="Region",
        title="Sales by Region"
    )

def profit_by_category(df):
    profit = df.groupby("Category")["Profit"].sum().reset_index()
    return px.bar(
        profit, x="Category", y="Profit", color="Category",
        title="Profit by Category"
    )

def top_customers(df, n=10):
    top = df.groupby("Customer Name")["Sales"].sum().nlargest(n).reset_index()
    return px.bar(
        top, x="Customer Name", y="Sales", color="Sales",
        title=f"Top {n} Customers"
    )