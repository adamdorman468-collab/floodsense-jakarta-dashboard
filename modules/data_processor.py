import pandas as pd

def process_flood_data(df):
    """Clean and format flood data for visualization."""
    df = df.dropna(subset=["lat", "lon"])
    df["status_color"] = df["status"].map({
        "Normal": "green",
        "Waspada": "orange",
        "Siaga": "red"
    }).fillna("blue")
    return df


def summarize_flood_stats(df):
    """Generate summary statistics for flood data."""
    summary = df["status"].value_counts().reset_index()
    summary.columns = ["Status", "Jumlah Lokasi"]
    return summary
