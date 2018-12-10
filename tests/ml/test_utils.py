import unittest
import itertools
import numpy as np
from parameterized import parameterized

from querio.ml.utils import *


class UtilsTest(unittest.TestCase):

    def test_make_into_set_makes_scalar_into_set(self):
        self.assertSetEqual({3}, make_into_set(3))

    def test_make_into_set_makes_list_into_set(self):
        list = [1, 2, 3, 4]
        self.assertSetEqual({1, 2, 3, 4}, make_into_set(list))

    def test_make_into_set_keeps_set_unchanged(self):
        set = {1, 2, 3, 4}
        self.assertSetEqual(set, make_into_set(set))

    @parameterized.expand([
        ('1', [[1, 2, 3], [4, 5, 6]]),
        ('2', [[6, 3, 4.6, 2, 7.5, 2], [3.5, 2], [7.8, 5, 1, 0], [1]]),
        ('3', [[1], [2], [3], [4]])
    ])
    def test_calculate_mean_and_variance_from_population(
        self, name, populations
    ):
        flattened = list(itertools.chain.from_iterable(populations))
        true_mean = np.mean(flattened)
        true_variance = np.var(flattened)

        param = [
            Population(len(pop), np.mean(pop), np.var(pop))
            for pop in populations
        ]
        mean, variance = calculate_mean_and_variance_from_populations(param)
        self.assertAlmostEqual(true_mean, mean)
        self.assertAlmostEqual(true_variance, variance)


if __name__ == '__main__':
    unittest.main()
