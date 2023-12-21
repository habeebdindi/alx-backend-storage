#!/usr/bin/env python3
"""This module contains a class"""
import redis
import uuid
from typing import Union, Callable, Optional, List
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """A decorator, tracks method call count"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """wrapper function to conserve original function name and docstring"""
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """A decorator, stores input and output history"""
    input_list_key = method.__qualname__ + ":inputs"
    output_list_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def set_history(self, *args, **kwds):
        """ Set list keys to wrapped function """
        self._redis.rpush(input_list_key, str(args))
        res = method(self, *args, **kwds)
        self._redis.rpush(output_list_key, str(res))
        return res

    return set_history


def replay(method: Callable) -> None:
    """ Ouput log of actions taken on method """
    counter_key = method.__qualname__
    input_list_key = method.__qualname__ + ':inputs'
    output_list_key = method.__qualname__ + ':outputs'
    this = method.__self__

    counter = this.get_str(counter_key)
    history = list(zip(this.get_list(input_list_key),
                       this.get_list(output_list_key)))
    print("{} was called {} times:".format(counter_key, counter))
    for call in history:
        value = this.get_str(call[0])
        key = this.get_str(call[1])
        print("{}(*{}) -> {}".format(counter_key, value, key))


class Cache:
    """Defines a cache class"""

    def __init__(self):
        """Initialization method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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

    def get_list(self, k: str) -> List:
        """ Convert bytes from store to list """
        return self._redis.lrange(k, 0, -1)
