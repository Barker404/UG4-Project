#!/usr/bin/env python

from random import random


def share_alg(shown):
    SHARE_PROB = 0.7
    return [x for x in shown if random() < SHARE_PROB]
