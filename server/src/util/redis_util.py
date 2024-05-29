import redis
import pickle
import logging
from typing import Any, Optional, Callable
from functools import wraps

from src.config import settings


logger = logging.getLogger(__name__)


class RedisCache:
    """
    Service class for caching data.
    """

    def __init__(self, host: str, port: str, db: int):
        """
        Initialize Redis cache service.

        :param host: Redis server host.
        :param port: Redis server port.
        :param db: Redis database number.
        """
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def set(
        self, key: str, data: dict[str, Any], expire_time: Optional[int] = None
    ) -> None:
        """
        Cache data with a key
        """
        try:
            serialized_data = pickle.dumps(data)
            self.redis_client.set(key, serialized_data, ex=expire_time)
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {e}")

    def get(self, key: str) -> Any:
        """
        Retrieve data from the cache for the given key
        """
        try:
            serialized_data = self.redis_client.get(key)

            if serialized_data:
                data = pickle.loads(serialized_data)
                return data
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {e}")

    def delete(self, key: str) -> None:
        """
        Delete data from the cache for the given key
        """
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {e}")


redis_cache = RedisCache(host=settings.redis.HOST, port=settings.redis.PORT, db=0)


def cache_data(key: str, expire_time: Optional[int] = None) -> Callable:
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for v in kwargs.values():
                cache_key = f"{key}:{v}"

            cached_data = redis_cache.get(cache_key)
            if cached_data:
                logger.debug(f"Cached data from Redis with key: {cache_key}")
                return cached_data

            response = await func(*args, **kwargs)
            if response:
                redis_cache.set(cache_key, response, expire_time=expire_time)
                logger.debug(f"Sent data to Redis for key: {cache_key}")

            return response

        return wrapper

    return decorator
