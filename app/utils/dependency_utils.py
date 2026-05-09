from app.services import WeatherService, CacheService
from app.clients import WeatherClient
from app.clients.redis_client import get_redis_client
from app.config import settings

async def get_weather_service() -> WeatherService:
    """ Dependency injection for weather service """
    client = WeatherClient(
        base_url=settings.URL_BASE_WEATHER_API,
        path=settings.PATH_CITY_WEATHER,
        api_key=settings.WEATHER_API_KEY
    )
    
    redis_client = await get_redis_client()
    
    cache = CacheService(redis_client)
    return WeatherService(client, cache)
  