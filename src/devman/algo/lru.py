"""
create_time: 2025-06-22 16:12:08
author: jackylee
"""

from collections import OrderedDict

import pytest

# from cachetools import LRUCache
# TODO 了解其功能


class LRU:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str):
        if key not in self.cache.keys():
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, val: str):
        if key in self.cache.keys():
            self.cache.move_to_end(key)
        self.cache[key] = val
        if len(self.cache) > self.capacity:
            self.cache.popitem(False)


def test_1(self):
    lru = LRU(3)
    self.assertListEqual(list(lru.cache.keys()), [])
    lru.put("a", "A")
    self.assertListEqual(list(lru.cache.keys()), ["a"])
    self.assertEqual(lru.get("a"), "A")
    lru.put("b", "B")
    self.assertListEqual(list(lru.cache.keys()), ["a", "b"])
    lru.put("c", "C")
    self.assertListEqual(list(lru.cache.keys()), ["a", "b", "c"])
    lru.put("d", "D")
    self.assertListEqual(list(lru.cache.keys()), ["b", "c", "d"])


def test_2(self):
    lru = LRU(3)
    self.assertListEqual(list(lru.cache.keys()), [])
    lru.put("a", "A")
    self.assertListEqual(list(lru.cache.keys()), ["a"])
    lru.put("b", "B")
    self.assertListEqual(list(lru.cache.keys()), ["a", "b"])
    lru.put("c", "C")
    self.assertListEqual(list(lru.cache.keys()), ["a", "b", "c"])
    lru.put("a", "A")
    self.assertListEqual(list(lru.cache.keys()), ["b", "c", "a"])


if __name__ == "__main__":
    pytest.main(["-vs", __file__])
