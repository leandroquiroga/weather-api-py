import redis.asyncio as redis
from app.config import settings

_redis_client = None


async def get_redis_client():
    """Get a singleton Redis client instance."""
    global _redis_client 
    if _redis_client is None:
            _redis_client = redis.ConnectionPool.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
                decode_responses=True
            )
    return redis.Redis(connection_pool=_redis_client)