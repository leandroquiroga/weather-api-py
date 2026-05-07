from fastapi import APIRouter, Depends, HTTPException ,status, Request
from models.weather_models import WeatherData
from middlewares.rate_limit_middleware import limiter
from utils import get_weather_service
from config import settings

weather_router = APIRouter(prefix="/v1/weather", tags=["weather"])

@weather_router.get("/{city}", response_model=WeatherData | str, status_code=status.HTTP_200_OK)
@limiter.limit(settings.RATE_LIMIT)
async def get_weather(request: Request, city: str, service = Depends(get_weather_service)):
    """ Endpoint to get weather data for a specific city. """
    try:
        return await service.get_weather_data(city)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))