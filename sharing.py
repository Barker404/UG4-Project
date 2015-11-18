#!/usr/bin/env python

import random

SHARE_AMOUNT = 5


def share_alg(shown):
    shared = set()

    while len(shared) < SHARE_AMOUNT and len(shown) > 0:
        item = random.choice(shown)
        shown.remove(item)
        shared.add(item[0])

    return list(shared)
