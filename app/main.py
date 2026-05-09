from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.utils.errors.exceptions_handlers import (
    handle_city_not_found,
    handle_external_api_exception,
    handle_cache_exception,
    handle_invalid_city_name
)

from app.utils.errors.custom_exceptions import (
    CityNotFoundError,
    ExternalAPIException,
    CacheException,
    InvalidCityNameError
)

from app.routes.weather_router import weather_router
from app.middlewares.rate_limit_middleware import limiter
from app.clients.redis_client import get_redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    redis_client = await get_redis_client()
    app.state.redis = redis_client
    yield
    # Shutdown
    await app.state.redis.close()
    


app = FastAPI(
    title="Weather API",
    description="A simple API to fetch weather data for a given city.",
    version="1.0.0",
    lifespan=lifespan
)



app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(CityNotFoundError, handle_city_not_found)
app.add_exception_handler(ExternalAPIException, handle_external_api_exception)
app.add_exception_handler(CacheException, handle_cache_exception)
app.add_exception_handler(InvalidCityNameError, handle_invalid_city_name)


app.include_router(weather_router)
