import requests
import pandas as pd
from datetime import datetime
from .utils import handle_error

# --- BMKG Weather API (example endpoint or fallback OpenWeatherMap)
def fetch_weather(city_name="Jakarta"):
    """Fetch current weather data from OpenWeatherMap (fallback if BMKG unavailable)."""
    try:
        api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # replace with your key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": datetime.now()
        }
    except Exception as e:
        handle_error("Weather API", e)
        return None


# --- Jakarta Smart City Flood Points API ---
def fetch_flood_data():
    """Fetch real-time flood data (dummy dataset if API not public)."""
    try:
        url = "https://data.jakarta.go.id/api/flood"  # example endpoint, replace as needed
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise Exception("API not accessible or outdated")

        df = pd.DataFrame(response.json()["data"])
        return df

    except Exception as e:
        # Fallback mock data (if API closed)
        handle_error("Flood API", e)
        data = {
            "location": ["Cempaka Putih", "Grogol", "Kebayoran Lama"],
            "status": ["Normal", "Waspada", "Siaga"],
            "lat": [-6.183, -6.160, -6.240],
            "lon": [106.865, 106.785, 106.782],
            "updated_at": [datetime.now()] * 3
        }
        return pd.DataFrame(data)
