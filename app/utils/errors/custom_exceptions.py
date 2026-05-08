class CityNotFoundError(Exception):
    """ Custom exception errors when a city is not found """
    def __init__(self, city: str):
        self.city = city
        super().__init__(f"City '{city}' not found.")

class ExternalAPIException(Exception):
    """ Custom exception for errors from external API calls """
    def __init__(self, message: str):
        super().__init__(f"External API error: {message}.")

class CacheException(Exception):
    """ Custom exception for cache errors """
    def __init__(self, operation: str, key: str, original_error: str | None = None):
        self.operation = operation
        self.key = key
        self.original_error = original_error
        message = f"Cache error during {operation} operation for key '{key}'."
        if original_error:
            message += f" Original error: {original_error}"
        super().__init__(message)
        
class InvalidCityNameError(Exception):
    """ Custom exception for invalid city name """
    def __init__(self, city: str):
        self.city = city
        super().__init__(f"Invalid city name: '{city}'. City names should only contain letters.")