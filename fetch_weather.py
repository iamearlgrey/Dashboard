"""
Pulls 7-day high/low from Open-Meteo. Free, no API key, no signup.
Docs: https://open-meteo.com/en/docs
"""

from __future__ import annotations

from datetime import date, datetime

import requests

from models import DayWeather
from config import WEATHER_LATITUDE, WEATHER_LONGITUDE, TEMPERATURE_UNIT

# WMO weather codes -> short label, just the common ones
_WMO = {
    0: "Clear", 1: "Mostly Clear", 2: "Partly Cloudy", 3: "Cloudy",
    45: "Fog", 48: "Fog", 51: "Drizzle", 53: "Drizzle", 55: "Drizzle",
    61: "Rain", 63: "Rain", 65: "Heavy Rain", 71: "Snow", 73: "Snow",
    75: "Heavy Snow", 80: "Showers", 81: "Showers", 82: "Showers",
    95: "Storms", 96: "Storms", 99: "Storms",
}

API_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_by_date() -> dict[date, DayWeather]:
    params = {
        "latitude": WEATHER_LATITUDE,
        "longitude": WEATHER_LONGITUDE,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "temperature_unit": TEMPERATURE_UNIT,
        "timezone": "auto",
        "forecast_days": 7,
    }
    resp = requests.get(API_URL, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()["daily"]

    out = {}
    for i, day_str in enumerate(data["time"]):
        d = datetime.strptime(day_str, "%Y-%m-%d").date()
        out[d] = DayWeather(
            high=data["temperature_2m_max"][i],
            low=data["temperature_2m_min"][i],
            condition=_WMO.get(data["weathercode"][i], ""),
        )
    return out
