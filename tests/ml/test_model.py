import unittest
import pandas as pd
import numpy as np
from parameterized import parameterized

from application.ml import Model


class ModelTest(unittest.TestCase):

    def setUp(self):
        ages = [22, 44, 36, 64]
        incomes = [age * 301 for age in ages]
        heights = [age * 50 for age in ages]
        self.data = pd.DataFrame(
            {'age': ages, 'income': incomes, 'height': heights}
        )
        self.models = {
            'One feature': Model(self.data, 'age', 'income'),
            'Two features': Model(
                self.data, ['age', 'height'], 'income'
            )
        }

    @parameterized.expand([
        ('One feature', 35),
        ('Two features', [35, 120]),
        ('One feature', {'age': 40}),
        ('Two features', {'age': 35, 'height': 120}),
    ])
    def test_predict_gives_value_in_correct_range(self, name, test_values):
        prediction, variance = self.models[name].predict(
            test_values
        )
        self.assertGreaterEqual(prediction, self.data['income'].min())
        self.assertLessEqual(prediction, self.data['income'].max())
        self.assertGreaterEqual(variance, 0)

    @parameterized.expand([
        ('One feature'),
        ('Two features'),
    ])
    def test_train_score_is_sensible(self, name):
        score = self.models[name].get_score_for_train()
        self.assertLessEqual(score, 1)

    @parameterized.expand([
        ('One feature'),
        ('Two features'),
    ])
    def test_test_score_is_sensible(self, name):
        score = self.models[name].get_score_for_test()
        self.assertLessEqual(score, 1)


if __name__ == '__main__':
    unittest.main()
