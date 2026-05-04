from pydantic import BaseModel

class WeatherData(BaseModel):
    """DTO for weather data"""
    coord: dict[str, float]
    weather: list[dict[str, int | str]]
    base: str
    main: dict[str, float | int]
    visibility: int
    wind: dict[str, float | int]
    clouds: dict[str, int]
    dt: int
    sys: dict[str, int | str]
    id: int
    name: str
    cod: int


    