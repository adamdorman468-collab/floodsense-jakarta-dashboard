# modules/data_processor.py
import pandas as pd

STATUS_COLOR_MAP = {
    "Normal": "green",
    "Waspada": "orange",
    "Siaga": "red",
    "Berbahaya": "darkred"
}

def process_flood_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure schema & add status_color. Return DataFrame.
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["location", "status", "lat", "lon", "updated_at", "status_color"])

    # Ensure types
    df = df.copy()
    df["location"] = df["location"].fillna("Unknown")
    df["status"] = df["status"].fillna("Unknown")
    # lat/lon numeric
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    if "updated_at" in df.columns:
        df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce").fillna(pd.Timestamp.utcnow())
    else:
        df["updated_at"] = pd.Timestamp.utcnow()

    df["status_color"] = df["status"].map(STATUS_COLOR_MAP).fillna("blue")
    # Drop rows without coords (we still return them; map code will skip None coords)
    return df


def summarize_flood_stats(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame({"Status": [], "Jumlah Lokasi": []})
    summary = df["status"].value_counts().reset_index()
    summary.columns = ["Status", "Jumlah Lokasi"]
    return summary
