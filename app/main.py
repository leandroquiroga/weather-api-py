from fastapi import FastAPI
from routes.weather_router import weather_router

app = FastAPI(
    title="Weather API",
    description="A simple API to fetch weather data for a given city.",
    version="1.0.0",
)


app.include_router(weather_router)
