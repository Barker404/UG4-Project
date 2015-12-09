#!/usr/bin/env python

import random
from abc import ABCMeta, abstractmethod


class ShareModel(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def share_alg(self, shown):
        pass


class BasicShareModel(ShareModel):

    def __init__(self, share_amount=5):
        self.share_amount = share_amount

    def share_alg(self, shown):
        shared = set()

        while len(shared) < self.share_amount and len(shown) > 0:
            item = random.choice(shown)
            shown.remove(item)
            shared.add(item[0])

        return list(shared)


class ProbShareModel(ShareModel):

    def __init__(self, share_prob=0.5):
        self.share_prob = share_prob

    def share_alg(self, shown):

        shared = set()

        for item in shown:
            # Messages shown more than once are more likely to be picked
            if random.random < self.share_prob:
                shared.add(item[0])

        return list(shared)
