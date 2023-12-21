#!/usr/bin/env python3
"""This module contains a class"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """Defines a cache class
    """

    def __init__(self):
        """Initialization method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """method that takes a data argument and returns a string"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes,
                                                                    int, None]:
        """method that take a key string argument and an optional Callable
        argument named fn"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """automatically parametrize Cache.get with the correct conversion
        function."""
        return self.get(key, fn=lambda d: d.decode('utf-8')
                        if isinstance(d, bytes) else None)

    def get_int(self, key: str) -> Union[int, None]:
        """parameterize get with int conversion function
        """
        return self.get(key, fn=lambda d: int(d)
                        if isinstance(d, bytes) else None)
