import httpx
from typing import Dict, Any
from app.config.setting_config import settings
from app.utils.security_utils import mask_sensitive_data, sanitize_error_message
from app.middlewares.logging_middleware import get_logger
from app.utils.errors.custom_exceptions import CityNotFoundError, ExternalAPIException

logger = get_logger(__name__)

class WeatherClient:
    """ 
    Client to interact with the WeatherAPI to fetch current weather data for a city.
    Args:
        - base_url: URL base of the Weather API
        - path: Path to fetch the weather data for a city
        - api_key: API key to authenticate requests
    """
    def __init__(self, base_url: str, path: str, api_key: str):
        self.base_url = base_url
        self.path = path
        self.api_key = api_key
        
    async def get_current_weather(self, city: str) -> Dict[str, Any]:
        """Get the current weather for the provided city

        Args:
            city (str): Name of the city

        Returns:
            Dictionary with the weather information from the OpenWeatherMap API
            
        Raises:
            httpx.HTTPStatusError: When API returns error status (sanitized)
            httpx.TimeoutException: When request times out
        """
        
        url = f"{self.base_url}{self.path}"
        params = {
            "q": city,
            "appid": self.api_key,
            "lang": settings.WEATHER_LANG,
            "units": settings.WEATHER_UNITS
        }
        
        # Logging with masked API key
        masked_params = mask_sensitive_data(params, sensitive_keys=["appid"])
        logger.info(f"Fetching weather data for city: {city} with params: {masked_params}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            sanitized_msg = sanitize_error_message(str(e), self.api_key)
            logger.error(f"HTTP error fetching weather for {city}: {sanitized_msg}")
            
            if e.response.status_code == 404:
                raise CityNotFoundError(city)
            elif e.response.status_code in [500, 502, 503, 504]:
                raise ExternalAPIException("Weather service is temporarily unavailable")
            else:
                raise ExternalAPIException(f"Unexpected API error: {e.response.status_code}")

        except httpx.TimeoutException as e:
            logger.error(f"Timeout fetching weather for {city}")
            raise ExternalAPIException("Weather service timeout")