import os
import requests
from typing import Dict

API_KEY = "Your_OpenWeatherMap_API_Key"
BASE_URL1 = "https://api.openweathermap.org/data/2.5/forecast"

def get_weather_forecast(lat: float, lon: float) -> Dict:
    if API_KEY == "Your_OpenWeatherMap_API_Key":
        return {
            "forecast": [],
            "city": "Unknown",
            "country": "",
            "error": "API key missing"
        }

    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL1, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        forecast = []
        for item in data["list"][:7]:
            forecast.append({
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "description": item["weather"][0]["description"],
                "wind_speed": item["wind"]["speed"]
            })

        return {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecast": forecast
        }

    except Exception as e:
        return {
            "forecast": [],
            "city": "Unknown",
            "country": "",
            "error": str(e)
        }
