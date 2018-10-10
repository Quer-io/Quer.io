import unittest
import itertools
import numpy as np
from parameterized import parameterized

from application.ml.utils import *


class UtilsTest(unittest.TestCase):

    def test_make_into_lest_if_scalar_makes_scalar_into_list(self):
        self.assertListEqual([3], make_into_list_if_scalar(3))

    def test_make_into_lest_if_scalar_keeps_list_unchanged(self):
        list = [1, 2, 3, 4]
        self.assertListEqual(list, make_into_list_if_scalar(list))

    @parameterized.expand([
        ('1', [[1, 2, 3], [4, 5, 6]]),
        ('2', [[6, 3, 4.6, 2, 7.5, 2], [3.5, 2], [7.8, 5, 1, 0], [1]]),
        ('3', [[1], [2], [3], [4]])
    ])
    def test_calculate_mean_and_variance_from_population(self, name, populations):
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
