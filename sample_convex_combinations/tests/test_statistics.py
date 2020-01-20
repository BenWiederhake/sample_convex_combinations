#!/usr/bin/env python3
# Copyright (c) 2020, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.


import sample_convex_combinations
import unittest


GATHER_FALSE_POSITIVE = 1e-10


def gather(d, span_origin, asserter):
    actual = sample_convex_combinations.sample(d, span_origin=span_origin)

    # Various sanity-checks:
    asserter.assertEqual(d, len(actual), actual)
    asserter.assertTrue(all(0.0 <= e <= 1.0 for e in actual), actual)
    if span_origin:
        # The following will fail 0.0002% of the time for no reason.
        # TODO: Find a better way to deal with it.
        asserter.assertTrue(GATHER_FALSE_POSITIVE <= sum(actual) <= 1 - GATHER_FALSE_POSITIVE, actual)
    else:
        asserter.assertAlmostEqual(1.0, sum(actual), actual)

    return actual


def gather_many(d, span_origin, asserter, n):
    return [gather(d, span_origin, asserter) for _ in range(n)]


def quantilify_each(dataset):
    transverse = [list(e) for e in zip(*dataset)]
    for column in transverse:
        column.sort()
    result = [e for e in zip(*transverse)]
    return result


def write_quantified(d, span_origin, n, filename):
    dataset = quantilify_each(gather_many(d, span_origin, unittest.TestCase(), n))
    with open(filename, 'w') as fp:
        for (i, sample) in enumerate(dataset):
            fp.write(' '.join(str(e) for e in [i / n, *sample]))
            fp.write('\n')


def write_samples(d, span_origin, n, filename):
    dataset = gather_many(d, span_origin, unittest.TestCase(), n)
    with open(filename, 'w') as fp:
        for sample in dataset:
            fp.write(' '.join(str(e) for e in sample))
            fp.write('\n')


class TestStatistics(unittest.TestCase):
    def test_dimensions(self):
        for d in [1, 2, 3, 5, 10]:
            for span_origin in [True, False]:
                with self.subTest(d=d, span_origin=span_origin):
                    self.run_test(d, span_origin)

    def run_test(self, d, span_origin):
        gather(d, span_origin, self)

