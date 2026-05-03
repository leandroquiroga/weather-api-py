from fastapi import APIRouter, Depends, HTTPException ,status
from models.weather_models import WeatherData
from utils import get_weather_service


weather_router = APIRouter(prefix="/v1/weather", tags=["weather"])

@weather_router.get("/{city}", response_model=WeatherData | str, status_code=status.HTTP_200_OK)
async def get_weather(city: str, service = Depends(get_weather_service)):
    """ Endpoint to get weather data for a specific city. """
    try:
        return await service.get_weather_data(city)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))