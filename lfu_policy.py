import logging
from policy import Policy, CacheManager, Cache


class LFU_Policy(Policy):
    def __init__(self, num_caches, cache_size, num_items):
        super(LFU_Policy, self).__init__(num_caches, cache_size, num_items, LFU_CacheManager)


class LFU_CacheManager(CacheManager):
    def __init__(self, num_caches, cache_size, num_items):
        super(LFU_CacheManager, self).__init__(num_caches, cache_size, num_items, LFU_Cache)

class LFU_Cache(Cache):
    def __init__(self, cache_size):
        self.size = cache_size
        self.count = 0
        self.items = set()
        self.cached_items = list()
        self.freqs = dict()

    def insert(self, new_item):
        self.items.add(new_item)
        self.freqs[new_item] = 0
        self.count += 1

    def access(self, new_item):
        cached = self.is_cached(new_item)
        old_item = None
        self.freqs[new_item] += 1
        if not(cached) and len(self.cached_items) < self.size:
            self.cached_items.append(new_item)
        elif not cached:
            old_item_idx = 0
            min_freq = 0
            for i in range(len(self.cached_items)):
                item = self.cached_items[i]
                if min_freq == 0 or self.freqs[item] < min_freq:
                    min_freq = self.freqs[item]
                    old_item = item
                    old_item_idx = i
            # Replace old item
            self.cached_items[old_item_idx] = new_item
        return (cached, old_item)

    def is_cached(self, item):
        return item in self.cached_items
