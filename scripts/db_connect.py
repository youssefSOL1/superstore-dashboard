from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

# --- Load credentials from .env ---
load_dotenv()
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")
DATABASE = os.getenv("DB_NAME")

def get_engine():
    """Create and return a PostgreSQL engine."""
    return create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

def load_data(table="orders"):
    """Load table from PostgreSQL into pandas DataFrame and enrich it."""
    engine = get_engine()
    df = pd.read_sql(f"SELECT * FROM {table};", engine)

    # --- Data Cleaning & Feature Engineering ---
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        df["Year"] = df["Order Date"].dt.year
        df["Month"] = df["Order Date"].dt.month
        df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)

    if "Sales" in df.columns and "Profit" in df.columns:
        df["Profit Margin"] = (df["Profit"] / df["Sales"]).round(2)

    return df
