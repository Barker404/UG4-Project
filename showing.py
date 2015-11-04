#!/usr/bin/env python

from collections import Counter


def show_alg(possible):
    counts = Counter(possible)
    top = counts.most_common(3)

    return [t[0] for t in top]
