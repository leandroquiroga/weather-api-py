from fastapi.responses import JSONResponse
from app.middlewares.logging_middleware import get_logger

logger = get_logger(__name__)

def handle_city_not_found(request, exc):
    """ Exception handler for CityNotFoundError """
    logger.error(f"City not found: {exc.city}")
    return JSONResponse(
        status_code=404,
        content={
            "Error": f"City {exc.city} not found. Please check the city name and try again.",
            "code": "CITY_NOT_FOUND"
        },
    )
    
def handle_external_api_exception(request, exc):
    """ Exception handler for ExternalAPIException """
    logger.error(f"External API error: {exc}")
    return JSONResponse(
        status_code=503,
        content={
            "Error": f"External API error: {exc}",
            "code": "EXTERNAL_API_ERROR"
        },
    )
def handle_cache_exception(request, exc):
    """ Exception handler for CacheException """
    logger.error(f"Cache error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "Error": f"Cache error during {exc.operation} operation for key '{exc.key}'.",
            "code": "CACHE_ERROR"
        },
    )
    
def handle_invalid_city_name(request, exc):
    """ Exception handler for InvalidCityNameError """
    logger.error(f"Invalid city name: {exc.city}")
    return JSONResponse(
        status_code=400,
        content={
            "Error": f"Invalid city name: '{exc.city}'. City names should only contain letters.",
            "code": "INVALID_CITY_NAME"
        },
    )