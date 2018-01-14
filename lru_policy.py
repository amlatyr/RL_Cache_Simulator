import logging
from collections import deque

from policy import Policy, CacheManager, Cache


class LRU_Policy(Policy):
    def __init__(self, num_caches, cache_size, num_items):
        super(LRU_Policy, self).__init__(num_caches, cache_size, num_items, LRU_CacheManager)


class LRU_CacheManager(CacheManager):
    def __init__(self, num_caches, cache_size, num_items):
        super(LRU_CacheManager, self).__init__(num_caches, cache_size, num_items, LRU_Cache)


class LRU_Cache(Cache):
    def __init__(self, cache_size):
        self.size = cache_size
        self.count = 0
        self.items = set()
        self.cached_items = deque()

    def insert(self, new_item):
        self.items.add(new_item)
        self.count += 1

    def access(self, new_item):
        cached = self.is_cached(new_item)
        old_item = None
        if cached:
            self.cached_items.remove(new_item)
            self.cached_items.appendleft(new_item)
        elif len(self.cached_items) < self.size:
            self.cached_items.appendleft(new_item)
        else:
            old_item = self.cached_items.pop()
            self.cached_items.appendleft(new_item)
        return (cached, old_item)

    def is_cached(self, item):
        return item in self.cached_items
