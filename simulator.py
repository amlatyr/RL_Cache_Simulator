import sys
import logging
import numpy as np

from requester import Requester
from lru_policy import LRU_Policy
from lfu_policy import LFU_Policy
from rnd_policy import RND_Policy

class Simulator:
    def __init__(self, requester=None, policy=None, num_item=100, cache_size=10, num_caches=1, num_requests=200):
        self.requester = requester
        self.policy = policy
        self.num_item = num_item
        self.cache_size = cache_size
        self.num_caches = num_caches
        self.num_requests = num_requests

    def run(self):
        for i in range(self.num_requests):
            new_request = self.requester.make_request()
            self.policy.execute_request(new_request)

if __name__ == "__main__":
    num_item = int(sys.argv[1])
    alpha = float(sys.argv[2])
    cache_size = int(sys.argv[3])
    num_caches = int(sys.argv[4])
    num_requests = int(sys.argv[5])
    requester = Requester(num_item, alpha)
    policy = LRU_Policy(num_caches, cache_size, num_item)
    sim = Simulator(requester, policy, num_item, cache_size, num_caches, num_requests)
    sim.run()
    print(num_item, alpha, cache_size, num_caches, num_requests)
