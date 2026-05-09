from app.services import WeatherService, CacheService
from app.clients import WeatherClient
from app.config import settings
import redis.asyncio as redis

def get_weather_service() -> WeatherService:
    """ Dependency injection for weather service """
    client = WeatherClient(
        base_url=settings.URL_BASE_WEATHER_API,
        path=settings.PATH_CITY_WEATHER,
        api_key=settings.WEATHER_API_KEY
    )
    
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True
    )
    
    cache = CacheService(redis_client)
    return WeatherService(client, cache)
  