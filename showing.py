#!/usr/bin/env python

from collections import Counter


def ShowAlg(possible):
    counts = Counter(possible)
    top = counts.most_common(3)

    return [t[0] for t in top]
