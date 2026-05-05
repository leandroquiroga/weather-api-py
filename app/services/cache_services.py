import json
from typing import Dict, Any

class CacheService: 
    """Service for managing Redis cache operations."""
    
    def __init__(self, redis_client):
        """
        Initialize cache service with Redis client.
        
        Args:
            redis_client: Async Redis client instance
        """
        self.redis_client = redis_client
        
    async def get_cache(self, key: str) -> dict | None:
        """
        Get cached data for a specific key.
        
        Args:
            key: Cache key to retrieve
            
        Returns:
            Cached data as dictionary or None if not found
        """
        data = await self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None
      
    async def set_cache(self, key: str, value: Dict[str, Any], expires: int) -> None:
        """
        Set cache data for a specific key with expiration.
        
        Args:
            key: Cache key
            value: Data to cache (will be JSON serialized)
            expires: TTL in seconds
        """
        await self.redis_client.set(key, json.dumps(value), ex=expires)
        
    async def delete_cache(self, key: str) -> None:
        """
        Delete cached data for a specific key.
        
        Args:
            key: Cache key to delete
        """
        await self.redis_client.delete(key)