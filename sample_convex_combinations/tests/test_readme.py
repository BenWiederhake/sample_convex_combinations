#!/usr/bin/env python3
# Copyright (c) 2020, Ben Wiederhake
# MIT license.  See the LICENSE file included in the package.

import sample_convex_combinations
import unittest


class TestBasic(unittest.TestCase):
    def test_call(self):
        self.assertEqual(3, len(sample_convex_combinations.sample(3)))

    def test_dimensions(self):
        for d in [1, 2, 3, 5, 10, 12, 19, 30]:
            with self.subTest(d=d):
                actual = sample_convex_combinations.sample(d)
                self.assertEqual(d, len(actual), actual)
                self.assertTrue(all(0.0 <= e <= 1.0 for e in actual), actual)
                self.assertAlmostEqual(1, sum(actual), actual)


class TestOriginSpan(unittest.TestCase):
    def test_call(self):
        self.assertEqual(3, len(sample_convex_combinations.sample(3, span_origin=True)))

    def test_dimensions(self):
        for d in [1, 2, 3, 5, 10, 12, 19, 30]:
            with self.subTest(d=d):
                actual = sample_convex_combinations.sample(d, span_origin=True)
                self.assertEqual(d, len(actual), actual)
                self.assertTrue(all(0.0 <= e <= 1.0 for e in actual), actual)
                # The following will fail 0.0002% of the time for no reason.
                # TODO: Find a better way to deal with it.
                self.assertTrue(0.000001 <= sum(actual) <= 0.999999, actual)


def dummy_rng():
    return 0.5


class TestRNG(unittest.TestCase):
    def test_call(self):
        self.assertEqual(3, len(sample_convex_combinations.sample(3, rng=dummy_rng)))

    def test_dimensions(self):
        for d in [1, 2, 3, 5, 10, 12, 19, 30]:
            with self.subTest(d=d):
                actual = sample_convex_combinations.sample(d, rng=dummy_rng)
                self.assertEqual(d, len(actual), actual)
                self.assertTrue(all(0.0 <= e <= 1.0 for e in actual), actual)
                self.assertAlmostEqual(1, sum(actual), actual)
