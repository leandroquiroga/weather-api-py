from models.weather_models import WeatherData


def get_weather_mock(city: str) -> WeatherData | str:
    """Return mock weather data for a given city."""
    if city.lower() == "london":
        return WeatherData(
            coord={"lon": -0.1257, "lat": 51.5085},
            weather=[
                {
                    "id": 300,
                    "main": "Drizzle",
                    "description": "light intensity drizzle",
                    "icon": "09d",
                }
            ],
            base="stations",
            main={
                "temp": 280.32,
                "feels_like": 278.45,
                "temp_min": 279.15,
                "temp_max": 281.15,
                "pressure": 1012,
                "humidity": 81,
            },
            visibility=10000,
            wind={"speed": 4.1, "deg": 80},
            clouds={"all": 90},
            dt=1605182400,
            sys={
                "type": 1,
                "id": 1414,
                "country": "GB",
                "sunrise": 1605165600,
                "sunset": 1605199200,
            },
            id=2643743,
            name="London",
            cod=200,
        )
    elif city.lower() == "new york":
        return WeatherData(
            coord={"lon": -74.006, "lat": 40.7128},
            weather=[
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "clear sky",
                    "icon": "01d",
                }
            ],
            base="stations",
            main={
                "temp": 295.15,
                "feels_like": 294.15,
                "temp_min": 293.15,
                "temp_max": 297.15,
                "pressure": 1013,
                "humidity": 60,
            },
            visibility=10000,
            wind={"speed": 3.6, "deg": 200},
            clouds={"all": 1},
            dt=1605182400,
            sys={
                "type": 1,
                "id": 1414,
                "country": "US",
                "sunrise": 1605165600,
                "sunset": 1605199200,
            },
            id=5128581,
            name="New York",
            cod=200,
        )
    else:
        return "City not found in mock data."
