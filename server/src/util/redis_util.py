import redis
import pickle
from typing import Any, Optional, Callable
from functools import wraps

from src.config import settings


class RedisCache:

    __REDIS_CLIENT = redis.Redis(
        host=settings.redis.HOST, port=settings.redis.PORT, db=0
    )

    @classmethod
    def set_cache(
        cls, key: str, data: dict[str, Any], expire_time: Optional[int] = None
    ) -> None:
        """
        Cache data with a key
        """
        serialized_data = pickle.dumps(data)

        cls.__REDIS_CLIENT.set(key, serialized_data, ex=expire_time)

    @classmethod
    def get_cache(cls, key: str) -> Any:
        """
        Retrieve data from the cache for the given key
        """
        serialized_data = cls.__REDIS_CLIENT.get(key)

        if serialized_data is None:
            return None

        data = pickle.loads(serialized_data)

        return data

    @classmethod
    def delete_cache(cls, key: str) -> None:
        """
        Delete data from the cache for the given key
        """
        cls.__REDIS_CLIENT.delete(key)


def cache_data(key: str, expire_time: Optional[int] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for v in kwargs.values():
                cache_key = f"{key}:{v}"

            cached_data = RedisCache.get_cache(cache_key)
            if cached_data is not None:
                return cached_data

            response = await func(*args, **kwargs)
            if response:
                RedisCache.set_cache(cache_key, response, expire_time=expire_time)

            return response

        return wrapper

    return decorator
