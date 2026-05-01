import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde el archivo .env


def _require_env(name: str) -> str:
    """ 
    Funcion para cargar las variables de entorno necesarias para el proyecto.
    Args:
        name (str): Nombre de la variable de entorno a cargar.  
    Returns: 
        str: Valor de la variable de entorno cargada.
    """
    
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Variable de entorno '{name}' no encontrada.")
    return value

WEATHER_API_KEY = _require_env("ACCESS_WEATHER_API_KEY")
REDIS_HOST = _require_env("ACCESS_REDIS_HOST")
REDIS_PORT = int(_require_env("ACCESS_REDIS_PORT"))
REDIS_DB = int(_require_env("ACCESS_REDIS_DB"))
CACHE_TTL_SECONDS = int(_require_env("ACCESS_CACHE_TTL_SECONDS"))