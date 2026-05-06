import httpx
from typing import Dict, Any
from utils.security_utils import mask_sensitive_data, sanitize_error_message
from middlewares.logging_middleware import get_logger

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
            "lang": "es",
            "units": "metric"  # Temperature in Celsius
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
            # Sanitized error message for logging
            sanitized_msg = sanitize_error_message(str(e), self.api_key)
            logger.error(f"HTTP error fetching weather for {city}: {sanitized_msg}")
            # Re-raise the error with sanitized message 
            raise httpx.HTTPStatusError(
                sanitized_msg,
                request=e.request,
                response=e.response
            )
        except httpx.TimeoutException as e:
            logger.error(f"Timeout fetching weather for {city}")
            raise
        except Exception as e:
            # Sanitized any unexpected error 
            sanitized_msg = sanitize_error_message(str(e), self.api_key)
            logger.error(f"Unexpected error fetching weather for {city}: {sanitized_msg}")
            raise Exception(sanitized_msg)
