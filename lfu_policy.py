import logging

class LFU_Policy:
    def __init__(self, num_caches, cache_size, num_items):
        self.cacheManager = LFU_CacheManager(num_caches, cache_size, num_items)
        logging.basicConfig(level=logging.DEBUG)
        self.num_misses = 0
        self.req_count = 0

    def execute_request(self, new_request):
        result = self.cacheManager.place(new_request)
        logging.info(" Item: %s, Cached: %s", str(new_request), str(result[0]))
        
        self.req_count += 1
        self.num_misses += not(result[0])
        if not result[0]:
            logging.info(" Evicted item is %s", str(result[1]))
        logging.log(" Miss Rate is %s", str(self.num_misses / self.req_count))

    
class LFU_CacheManager:
    def __init__(self, num_caches, cache_size, num_items):
        self.num_caches = num_caches
        self.cache_size = cache_size
        self.num_items = num_items
        self.caches = [LFU_Cache(cache_size) for i in range(num_caches)]

    def init_caches(self, num_items):
        for i in range(num_items):
            self.caches[i % self.num_caches].insert(i)

    def is_cached(self, item):
        return self.caches[item % self.num_caches].is_cached(item)

    def place(self, new_item):
        return self.caches[new_item % self.num_caches].place(new_item)


class LFU_Cache:
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

    def place(self, new_item):
        cached = self.is_cached(new_item)
        old_item = None
        if not cached:
            old_item_idx = 0
            min_freq = 0
            for i in range(len(self.cached_items)):
                item = self.cached_items[i]
                if self.freqs[item] < min_freq:
                    min_freq = self.freqs[item]
                    old_item = item
                    old_item_idx = i
            # Replace old item
            self.cached_items[old_item_idx] = new_item
        return (cached, old_item)

    def is_cached(self, item):
        return item in self.cached_items