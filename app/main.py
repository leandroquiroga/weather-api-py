from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from routes.weather_router import weather_router
from middlewares.logging_middleware import get_logger
from middlewares.rate_limit_middleware import limiter
app = FastAPI(
    title="Weather API",
    description="A simple API to fetch weather data for a given city.",
    version="1.0.0",
)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(weather_router)
