from clients import WeatherClient
from models import WeatherData


class WeatherService: 
    """ Business logic for fetching weather data."""
    
    def __init__(self, client: WeatherClient):
        """
        Initialize weather service with a weather client.
        
        Args:
            client (WeatherClient): An instance of WeatherClient to fetch weather data.
        """
        self.client = client
    
    async def get_weather_data(self, city: str) -> WeatherData:
        """ 
        Get weather data for a specific city.
        
        Args: 
            city (str): The name of the city
            
        Returns:
            WeatherData: An instance of WeatherData containing the weather information.
        """
        raw_data = await self.client.get_current_weather(city)
        return WeatherData(**raw_data)
      