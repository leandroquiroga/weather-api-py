from pydantic import BaseModel

class Coord(BaseModel):
    """DTO for coordinates"""
    lon: float
    lat: float
    
class WeatherCondition(BaseModel):
    """ DTO for weather condition"""
    id: int
    main: str
    description: str
    icon: str
    
class MainWeatherData(BaseModel):
    """ DTO for main weather data"""
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int | None = None
    grnd_level: int | None = None
    
class Wind(BaseModel):
    """ DTO for wind data"""
    speed: float
    deg: int
    gust: float | None = None
    
class Clouds(BaseModel):
    """ DTO for cloud data"""
    all: int
    
class Sys(BaseModel):
    """ DTO for system data"""
    type: int
    id: int
    country: str
    sunrise: int
    sunset: int
class WeatherData(BaseModel):
    """DTO for weather data"""
    coord: Coord
    weather: list[WeatherCondition]
    base: str
    main: MainWeatherData
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    id: int
    name: str
    cod: int


    