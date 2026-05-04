import httpx
from typing import Dict, Any

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
        """
        
        url = f"{self.base_url}{self.path}"
        params = {
            "q": city,
            "appid": self.api_key,
            "lang": "es",
            "units": "metric"  # Temperature in Celsius
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
