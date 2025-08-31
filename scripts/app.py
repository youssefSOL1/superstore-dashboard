import streamlit as st
import pandas as pd
from db_connect import load_data
from eda import preprocess_data
import viz

# --- Page Config ---
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

# --- Load & Preprocess Data ---
df = load_data("orders")
df = preprocess_data(df)

# --- Sidebar Navigation ---
st.sidebar.title("Superstore Dashboard")
page = st.sidebar.radio("Select Page", [
    "Overview", "Sales Analysis", "Profit Analysis",
    "Customer Analysis", "Forecasting", "Recommendations"
])

# --- Filters ---
st.sidebar.subheader("Filters")
min_date, max_date = df["Order Date"].min(), df["Order Date"].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
regions = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
categories = st.sidebar.multiselect("Select Category", df["Category"].unique(), default=df["Category"].unique())

mask = (
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1])) &
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
)
df_filtered = df.loc[mask]

# ================= Pages ================= #
if page == "Overview":
    st.title("📊 Superstore Dashboard")
    total_sales = df_filtered["Sales"].sum()
    total_profit = df_filtered["Profit"].sum()
    num_orders = df_filtered["Order ID"].nunique()
    avg_margin = df_filtered["Profit Margin"].mean()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Sales", f"${total_sales:,.0f}")
    kpi2.metric("Total Profit", f"${total_profit:,.0f}")
    kpi3.metric("Number of Orders", f"{num_orders:,}")
    kpi4.metric("Avg Profit Margin", f"{avg_margin:.2%}")

    st.plotly_chart(viz.sales_over_time(df_filtered), use_container_width=True)

elif page == "Sales Analysis":
    st.title("💰 Sales Analysis")
    st.plotly_chart(viz.sales_by_region(df_filtered), use_container_width=True)

elif page == "Profit Analysis":
    st.title("📈 Profit Analysis")
    st.plotly_chart(viz.profit_by_category(df_filtered), use_container_width=True)

elif page == "Customer Analysis":
    st.title("🧑‍🤝‍🧑 Customer Analysis")
    st.plotly_chart(viz.top_customers(df_filtered), use_container_width=True)

elif page == "Forecasting":
    st.title("🔮 Sales Forecasting")
    st.info("Future predictions will go here...")

elif page == "Recommendations":
    st.title("🏆 Recommendations")
    st.info("We’ll later use ML or rule-based logic to generate recommendations.")
