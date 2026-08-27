import httpx
from typing import Optional
from dataclasses import dataclass


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

NER_CITIES_WEATHER = [
    ("Guwahati", 26.1445, 91.7362),
    ("Shillong", 25.5788, 91.8933),
    ("Imphal", 24.8170, 93.9368),
    ("Agartala", 23.8315, 91.2869),
    ("Aizawl", 23.7271, 92.7176),
    ("Kohima", 25.6586, 94.1086),
    ("Gangtok", 27.3389, 88.6065),
    ("Itanagar", 27.0844, 93.6958),
    ("Dibrugarh", 27.4728, 94.9120),
    ("Silchar", 24.8333, 92.7789),
]


@dataclass
class WeatherData:
    city: str
    lat: float
    lon: float
    temperature_c: float
    rainfall_1h_mm: float
    rainfall_24h_mm: float
    wind_speed_kmh: float
    humidity_pct: float
    weather_code: int
    description: str


WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Light showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm + hail", 99: "Heavy hail storm",
}


async def get_weather(lat: float, lon: float) -> Optional[WeatherData]:
    params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,rain,weather_code,wind_speed_10m",
        "hourly": "rain",
        "forecast_days": 1,
        "timezone": "Asia/Kolkata",
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(OPEN_METEO_URL, params=params)
            if resp.status_code != 200:
                return None
            data = resp.json()
            current = data.get("current", {})
            hourly = data.get("hourly", {})
            rain_1h = hourly.get("rain", [0])
            code = current.get("weather_code", 0)
            return WeatherData(
                city="", lat=lat, lon=lon,
                temperature_c=current.get("temperature_2m", 0),
                rainfall_1h_mm=current.get("rain", 0),
                rainfall_24h_mm=sum(rain_1h) if rain_1h else 0,
                wind_speed_kmh=current.get("wind_speed_10m", 0),
                humidity_pct=current.get("relative_humidity_2m", 0),
                weather_code=code,
                description=WEATHER_CODES.get(code, "Unknown"),
            )
    except (httpx.ConnectError, httpx.TimeoutException):
        return None


async def get_ner_weather_dashboard() -> list[dict]:
    results = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        for city, lat, lon in NER_CITIES_WEATHER:
            params = {
                "latitude": lat, "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,rain,weather_code,wind_speed_10m",
                "hourly": "rain",
                "forecast_days": 1,
                "timezone": "Asia/Kolkata",
            }
            try:
                resp = await client.get(OPEN_METEO_URL, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    current = data.get("current", {})
                    hourly = data.get("hourly", {})
                    rain_1h = hourly.get("rain", [0])
                    code = current.get("weather_code", 0)
                    results.append({
                        "city": city,
                        "lat": lat, "lon": lon,
                        "temperature_c": current.get("temperature_2m", 0),
                        "rainfall_1h_mm": current.get("rain", 0),
                        "rainfall_24h_mm": sum(rain_1h) if rain_1h else 0,
                        "wind_speed_kmh": current.get("wind_speed_10m", 0),
                        "humidity_pct": current.get("relative_humidity_2m", 0),
                        "weather_code": code,
                        "description": WEATHER_CODES.get(code, "Unknown"),
                    })
            except (httpx.ConnectError, httpx.TimeoutException):
                results.append({"city": city, "lat": lat, "lon": lon, "error": "unavailable"})
    return results
