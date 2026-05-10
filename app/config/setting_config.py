from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configuration environment variables"""
    URL_BASE_WEATHER_API: str = Field(validation_alias="ACCESS_URL_BASE_WEATHER_API")
    PATH_CITY_WEATHER: str = Field(validation_alias="ACCESS_PATH_CITY_WEATHER")
    WEATHER_API_KEY: str = Field(validation_alias="ACCESS_WEATHER_API_KEY")
    REDIS_HOST: str = Field(validation_alias="ACCESS_REDIS_HOST")
    
    REDIS_PORT: int = Field(validation_alias="ACCESS_REDIS_PORT")
    REDIS_DB: int = Field(validation_alias="ACCESS_REDIS_DB")
    CACHE_TTL_SECONDS: int = Field(validation_alias="ACCESS_CACHE_TTL_SECONDS")
    WEATHER_LANG: str = Field(validation_alias="ACCESS_WEATHER_LANG")
    WEATHER_UNITS: str = Field(validation_alias="ACCESS_WEATHER_UNITS")
    
    RATE_LIMIT: str = Field(
      default="10/minute",
      validation_alias="ACCESS_RATE_LIMIT",
      description="Rate limit format: {count}/{period}"
    )
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
      
    )
    
settings = Settings()


