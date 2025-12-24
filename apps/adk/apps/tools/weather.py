
from typing import Literal
import httpx
from geopy.geocoders import Nominatim

def get_coordinates(city_name: str) -> tuple[float, float]:
    """도시 이름을 받아 위도와 경도를 반환 합니다."""
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError(f"Could not find coordinates for city: {city_name}")
    # coordinates = {
    #     "Seoul": (37.5665, 126.9780),
    #     "New York": (40.7128, -74.0060),
    #     "London": (51.5074, -0.1278),
    # }
    # return coordinates.get(city_name, (0.0, 0.0))

def get_weather(city_name: str) -> dict:
    """도시 이름을 받아 해당 도시의 현재 날시 정보를 반환합니다."""
    if city_name:
        latitude, longitude = get_coordinates(city_name)

        print(f"[Call Weather Tool]\nCoordinates for {city_name}: Latitude {latitude}, Longitude {longitude}")
    else:
        raise ValueError("City name must be provided")
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()
    # return {
    #     "city": city,
    #     "temperature": "22°C",
    #     "condition": "Sunny"
    # }