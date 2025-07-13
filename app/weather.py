import requests
from typing import Dict

API_KEY = "Your_OpenWeatherMap_API_Key"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_weather_forecast(lat: float, lon: float) -> Dict:
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    forecast = []
    for item in data["list"]:
        forecast.append({
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "description": item["weather"][0]["description"],
            "wind_speed": item["wind"]["speed"]
        })
    return {
        "city": data["city"]["name"],
        "country": data["city"]["country"],
        "forecast": forecast[:7]
    }
