import logging
import sys


# Configure logging global

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Set lower log levels for noisy libraries
logging.getLogger("httpx").setLevel(logging.WARNING)  
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Configure loggers - INFO level
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("fastapi").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """ 
      Get a logger instance with the specified name.
      
      Args: 
          name (str): The name of the logger, typically the module name.
          
      Returns: 
          A configured logger instance.
      
    """
    return logging.getLogger(name)
