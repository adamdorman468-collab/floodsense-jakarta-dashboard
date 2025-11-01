# modules/data_fetcher.py
import os
import requests
import pandas as pd
from datetime import datetime
import streamlit as st
from .utils import log_error

# Use Streamlit secrets or environment variables.
OPENWEATHERMAP_API_KEY = None
if st.secrets and "OPENWEATHERMAP_API_KEY" in st.secrets:
    OPENWEATHERMAP_API_KEY = st.secrets["OPENWEATHERMAP_API_KEY"]
else:
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")


def fetch_weather_openweathermap(city_name="Jakarta"):
    """
    Fetch current weather via OpenWeatherMap.
    Returns dict or None.
    """
    if not OPENWEATHERMAP_API_KEY:
        log_error("Weather API", Exception("No OpenWeatherMap API key configured"))
        return None

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city_name, "appid": OPENWEATHERMAP_API_KEY, "units": "metric"}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        result = {
            "city": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "humidity": data.get("main", {}).get("humidity"),
            "description": data.get("weather", [{}])[0].get("description"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "timestamp": datetime.utcfromtimestamp(data.get("dt")) if data.get("dt") else datetime.utcnow()
        }
        return result
    except Exception as e:
        log_error("Weather API", e)
        return None


# Flood data: try a configured FLOOD_API_URL in secrets or fallback to built-in sample
def fetch_flood_data():
    """
    Attempts to fetch flood points from configured API (set as FLOOD_API_URL in secrets).
    Returns a pandas DataFrame with columns: location, status, lat, lon, updated_at
    If API not available, returns a sample DataFrame.
    """
    flood_api_url = None
    if st.secrets and "FLOOD_API_URL" in st.secrets:
        flood_api_url = st.secrets["FLOOD_API_URL"]
    else:
        flood_api_url = os.getenv("FLOOD_API_URL")

    if flood_api_url:
        try:
            resp = requests.get(flood_api_url, timeout=10)
            resp.raise_for_status()
            payload = resp.json()
            # Expect standardized payload format or try to adapt common fields
            # Attempt to find an array of locations in payload
            if isinstance(payload, dict):
                # try common keys
                data = payload.get("data") or payload.get("results") or payload.get("features") or payload
            else:
                data = payload

            df = pd.json_normalize(data)
            # Try to standardize column names
            # Common names: name/location, status, lat/lon or geometry.coordinates
            # Normalize possible columns
            col_map = {}
            if "location" in df.columns:
                col_map["location"] = "location"
            elif "name" in df.columns:
                col_map["name"] = "location"

            if "status" in df.columns:
                col_map["status"] = "status"
            elif "severity" in df.columns:
                col_map["severity"] = "status"

            if "lat" in df.columns and "lon" in df.columns:
                col_map["lat"] = "lat"
                col_map["lon"] = "lon"
            elif "geometry.coordinates" in df.columns:
                # geometry.coordinates often [lon, lat]
                df[["geometry_lon", "geometry_lat"]] = pd.DataFrame(df["geometry.coordinates"].tolist(), index=df.index)
                col_map["geometry_lat"] = "lat"
                col_map["geometry_lon"] = "lon"

            # apply renaming if mapping exists
            if col_map:
                df = df.rename(columns={k: v for k, v in col_map.items()})

            # Keep required columns, fill missing
            for c in ["location", "status", "lat", "lon"]:
                if c not in df.columns:
                    df[c] = None

            # Timestamp
            if "updated_at" not in df.columns:
                df["updated_at"] = pd.Timestamp.utcnow()

            df = df[["location", "status", "lat", "lon", "updated_at"]]
            return df
        except Exception as e:
            log_error("Flood API", e)

    # Fallback sample data (guaranteed consistent schema)
    sample = [
        {"location": "Cempaka Putih", "status": "Normal", "lat": -6.183, "lon": 106.865, "updated_at": datetime.utcnow()},
        {"location": "Grogol", "status": "Waspada", "lat": -6.160, "lon": 106.785, "updated_at": datetime.utcnow()},
        {"location": "Kebayoran Lama", "status": "Siaga", "lat": -6.240, "lon": 106.782, "updated_at": datetime.utcnow()},
    ]
    return pd.DataFrame(sample)
