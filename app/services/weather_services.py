from clients import WeatherClient
from models import WeatherData
from services.cache_services import CacheService
from config import settings

class WeatherService: 
    """ Business logic for fetching weather data."""
    
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
        cached = await self.cache.get_cache(cache_key)
        
        if cached: 
            return WeatherData(**cached)
          
        raw_data = await self.client.get_current_weather(city)
        await self.cache.set_cache( cache_key, raw_data, expires=settings.CACHE_TTL_SECONDS )
        return WeatherData(**raw_data)
      
      