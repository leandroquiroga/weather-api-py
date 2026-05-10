from fastapi import APIRouter,Depends ,status, Request
from app.config import settings
from app.utils import get_weather_service
from app.models.weather_models import WeatherData
from app.middlewares.rate_limit_middleware import limiter
from app.utils.errors.custom_exceptions import InvalidCityNameError

weather_router = APIRouter(prefix="/v1/weather", tags=["weather"])

@weather_router.get("/{city}", response_model=WeatherData | str, status_code=status.HTTP_200_OK)
@limiter.limit(settings.RATE_LIMIT)
async def get_weather(request: Request, city: str, service = Depends(get_weather_service)):
    """ Endpoint to get weather data for a specific city. """
    if not city or city.strip() == "":
        raise InvalidCityNameError(city, "City name cannot be empty.")
    
    if len(city) > 50:
        raise InvalidCityNameError(city, "City name is too long.")
    
    if not city.replace(" ", "").replace("-", "").isalpha():
        raise InvalidCityNameError(city, "City names contains invalid characters.")
    
    return await service.get_weather_data(city)