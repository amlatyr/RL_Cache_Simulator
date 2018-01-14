import numpy as np


class Requester:
    def __init__(self, num_items, alpha):
        self.num_items = num_items
        self.alpha = alpha

    def make_request(self):
        next_request = np.random.zipf(self.alpha) - 1
        while next_request >= self.num_items:
            next_request = np.random.zipf(self.alpha) - 1
        return next_request
