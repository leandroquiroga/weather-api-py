from app.clients import WeatherClient
from app.models import WeatherData
from app.config import settings
from app.middlewares import get_logger
from app.services.cache_services import CacheService
from app.utils.errors.custom_exceptions import CacheException

logger = get_logger(__name__)


class WeatherService:
    """Business logic for fetching weather data."""

    def __init__(self, client: WeatherClient, cache: CacheService):
        """
        Initialize weather service with a weather client and cache service.

        Args:
            client (WeatherClient): An instance of WeatherClient to fetch weather data.
            cache (CacheService): An instance of CacheService to manage caching of weather data.
        """
        self.client = client
        self.cache = cache

    async def get_weather_data(self, city: str) -> WeatherData:
        """
        Get weather data for a specific city.

        Args:
            city (str): The name of the city

        Returns:
            WeatherData: An instance of WeatherData containing the weather information.
        """
        cache_key = f"weather:current:{city.lower()}"

        try:
            cached = await self.cache.get_cache(cache_key)
            if cached:
                logger.info(f"Cache hit for city: {city}")
                return WeatherData(**cached)
        except CacheException as e:
            logger.warning(f"Cache unavailable: {e}. Fetching from API without cache.")

        logger.info(f"Cache miss for city: {city}. Fetching from API.")
        raw_data = await self.client.get_current_weather(city)

        try:
            await self.cache.set_cache(
                cache_key, raw_data, expires=settings.CACHE_TTL_SECONDS
            )
            logger.info(f"Weather data for city: {city} cached successfully.")
        except CacheException as e:
            logger.warning(f"Failed to cache data for {city}: {e}")

        return WeatherData(**raw_data)
