"""
Update the native lru cache with a TTl
"""

from functools import lru_cache, wraps
from time import time
from typing import Callable


def lru_cache_ttl(maxsize=5, ttl=120):
    def decorator(func: Callable):
        func = lru_cache(maxsize=maxsize)(func)
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            result, timestamp = cache.get(key, (None, 0))
            if result is None or timestamp < time():
                result = func(*args, **kwargs)
                cache[key] = (result, time() + ttl)
            return result

        return wrapper

    return decorator
