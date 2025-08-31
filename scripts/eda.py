import pandas as pd
from db_connect import load_data

def basic_summary(df):
    """Return basic dataset info."""
    summary = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "dtypes": df.dtypes.to_dict(),
        "numeric_summary": df.describe().to_dict()
    }
    return summary

def preprocess_data(df):
    """Feature engineering for dashboard use."""
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Profit Margin"] = df["Profit"] / df["Sales"]
    df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)
    return df

if __name__ == "__main__":
    df = load_data("orders")
    df = preprocess_data(df)
    summary = basic_summary(df)
    print("Dataset Shape:", summary["shape"])
    print("\nMissing Values:", summary["missing_values"])
    print("\nDuplicates:", summary["duplicates"])
    print("\nNumeric Summary:\n", pd.DataFrame(summary["numeric_summary"]))
