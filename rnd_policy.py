import logging
import random
from policy import Policy, CacheManager, Cache

class RND_Policy(Policy):
    def __init__(self, num_caches, cache_size, num_items):
        super(RND_Policy, self).__init__(num_caches, cache_size, num_items, RND_CacheManager)

class RND_CacheManager(CacheManager):
    def __init__(self, num_caches, cache_size, num_items):
        super(RND_CacheManager, self).__init__(num_caches, cache_size, num_items, RND_Cache)

class RND_Cache(Cache):
    def __init__(self, cache_size):
        self.size = cache_size
        self.count = 0
        self.items = set()
        self.cached_items = list()

    def insert(self, new_item):
        self.items.add(new_item)
        self.count += 1

    def access(self, new_item):
        cached = self.is_cached(new_item)
        old_item = None
        if not(cached) and len(self.cached_items) < self.size:
            self.cached_items.append(new_item)
        elif not cached:
            idx = random.choice(range(0, self.size))
            old_item = self.cached_items[idx]
            self.cached_items[idx] = new_item
        return (cached, old_item)

    def is_cached(self, item):
        return item in self.cached_items
