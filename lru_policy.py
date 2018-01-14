import logging
from collections import deque

class LRU_Policy:
    def __init__(self, num_caches, cache_size, num_items):
        self.cacheManager = LRU_CacheManager(num_caches, cache_size, num_items)
        logging.basicConfig(level=logging.DEBUG)
        self.num_misses = 0
        self.req_count = 0

    def execute_request(self, new_request):
        result = self.cacheManager.access(new_request)
        logging.info(" Item: %s, Cached: %s", str(new_request), str(result[0]))

        self.req_count += 1
        self.num_misses += not(result[0])
        if not result[0]:
            logging.info(" Evicted item is %s", str(result[1]))
        print(str(self.num_misses / self.req_count))
        logging.info(" Miss Rate is %s", str(self.num_misses / self.req_count))


class LRU_CacheManager:
    def __init__(self, num_caches, cache_size, num_items):
        self.num_caches = num_caches
        self.cache_size = cache_size
        self.num_items = num_items
        self.caches = [LRU_Cache(cache_size) for i in range(num_caches)]
        self.init_caches()

    def init_caches(self):
        for i in range(self.num_items):
            self.caches[i % self.num_caches].insert(i)

    def is_cached(self, item):
        return self.caches[item % self.num_caches].is_cached(item)

    def access(self, new_item):
        return self.caches[new_item % self.num_caches].access(new_item)


class LRU_Cache:
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
