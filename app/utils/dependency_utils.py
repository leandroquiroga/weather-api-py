from services import WeatherService
from clients import WeatherClient
from config import settings

def get_weather_service() -> WeatherService:
    """ Dependency inyection for weather service """
    client = WeatherClient(
        base_url=settings.URL_BASE_WEATHER_API,
        path=settings.PATH_CITY_WEATHER,
        api_key=settings.WEATHER_API_KEY
    )
    return WeatherService(client)