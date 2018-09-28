import unittest
import pandas as pd

from application.ml import Model


class ModelTest(unittest.TestCase):

    def setUp(self):
        ages = [22, 44, 36, 64]
        incomes = [age * 301 for age in ages]
        self.data = pd.DataFrame({'age': ages, 'income': incomes})
        self.model = Model(self.data, 'age', 'income')

    def test_predict_gives_value_in_correct_range(self):
        prediction, variance = self.model.predict(35)
        self.assertGreaterEqual(prediction, self.data['income'].min())
        self.assertLessEqual(prediction, self.data['income'].max())

    def test_train_score_is_sensible(self):
        score = self.model.get_score_for_train()
        self.assertLessEqual(score, 1)

    def test_test_score_is_sensible(self):
        score = self.model.get_score_for_test()
        self.assertLessEqual(score, 1)


if __name__ == '__main__':
    unittest.main()
