# Copyright (c) 2020, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.
"""Samples from convex combination space.

In theory this module "only" provides a bit of math.
In practice, it's a useful piece of abstraction.

This module provides a function that pickes a convex combination of a
desired dimension (= number of items=, uniformly distributed among all
convex combinations. It is possible supply your own RNG, or a
hand-picked point from a hypercube (uniform distribution in the
hypercube guarantees uniform distribution in "convex
combination"-space).
"""

import random


def sample(d, span_origin=False, rng=random.random):
    remaining_volume = 1.0
    result = list()
    for i in range(d - 1 + span_origin):
        raise NotImplementedError()

    if span_origin:
        result.append(1 - sum(result))

    return result
