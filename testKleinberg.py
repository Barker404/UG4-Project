#!/usr/bin/env python

import timeit


print(timeit.timeit("graph.kleinberg(70, 70, 1, 2)",
                    setup="import graph", number=2))

print(timeit.timeit("graph.kleinberg2(70, 70, 1, 2)",
                    setup="import graph", number=2))
