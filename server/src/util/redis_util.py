import redis
import pickle
from typing import Any, Optional, Callable
from functools import wraps

from src.config import REDIS_HOST, REDIS_PORT


# class RedisCache:
#     def __init__(self):
#         self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

#     def set_cache(
#         self, key: str, data: dict[str, Any], expire_time: Optional[int] = None
#     ) -> None:
#         """
#         Cache data with a key
#         """
#         serialized_data = pickle.dumps(data)

#         self.redis_client.set(key, serialized_data, ex=expire_time)

#     def get_cache(self, key: str) -> Any:
#         """
#         Retrieve data from the cache for the given key
#         """
#         serialized_data = self.redis_client.get(key)

#         if serialized_data is None:
#             return None

#         data = pickle.loads(serialized_data)

#         return data

#     def del_cache(self, key: str) -> None:
#         """
#         Delete data from the cache for the given key
#         """
#         self.redis_client.delete(key)


class RedisCache:

    __REDIS_CLIENT = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

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

    def del_cache(cls, key: str) -> None:
        """
        Delete data from the cache for the given key
        """
        cls.__REDIS_CLIENT.delete(key)


def cache_data(key: str, expire_time: Optional[int] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{key}:{kwargs}"

            cached_data = RedisCache.get_cache(cache_key)
            if cached_data is not None:
                return cached_data

            response = await func(*args, **kwargs)
            if response:
                RedisCache.set_cache(cache_key, response, expire_time=expire_time)

            return response

        return wrapper

    return decorator


def update_cache_data(key: str, expire_time: Optional[int] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):

            response = await func(*args, **kwargs)
            cache_key = f"{key}:{response.author_id}"

            RedisCache.set_cache(cache_key, response, expire_time=expire_time)

            return response

        return wrapper

    return decorator
