import unittest
import pandas as pd
import numpy as np
from parameterized import parameterized

from querio.ml import Model
from querio.ml.utils import make_into_list_if_scalar


class ModelTest(unittest.TestCase):

    def setUp(self):
        ages = [22, 44, 36, 64, 32, 86, 11, 45]
        incomes = [age * 301 for age in ages]
        heights = [age * 50 for age in ages]
        github_stars = [age * 20 + 10 for age in ages]
        self.data = pd.DataFrame({
            'age': ages, 'income': incomes, 'height': heights,
            'github_stars': github_stars
        })
        self.models = {
            'One feature': Model(self.data, 'age', 'income'),
            'Two features': Model(
                self.data, ['age', 'height'], 'income'
            ),
            'Two features reverse': Model(
                self.data, ['height', 'age'], 'income'
            ),
            'Three features': Model(
                self.data, ['age', 'height', 'github_stars'], 'income'
            )
        }

    @parameterized.expand([
        ('One feature', 35),
        ('Two features', [35, 120]),
        ('One feature', {'age': 40}),
        ('Two features', {'age': 35, 'height': 120}),
    ])
    def test_predict_gives_value_in_correct_range(self, name, test_values):
        prediction = self.models[name].predict(
            test_values
        )
        self.assertGreaterEqual(prediction.result, self.data['income'].min())
        self.assertLessEqual(prediction.result, self.data['income'].max())
        self.assertGreaterEqual(prediction.variance, 0)

    @parameterized.expand([
        ('One feature', 40),
        ('Two features', [41, 134])
    ])
    def test_predict_same_mean_as_sklearn_predict(self, name, test_values):
        model = self.models[name]
        prediction = model.predict(test_values)
        test_values = make_into_list_if_scalar(test_values)
        self.assertAlmostEqual(
            model.tree.predict([test_values])[0],
            prediction.result
        )

    @parameterized.expand([
        ('1', {'age': 42}, 10535),
        ('2', {'age': 33, 'height': 100}, 7926.333333333333333),
        ('3', {'height': 120, 'github_stars': 54}, 3311),
        ('4', {'github_stars': 42}, 10685.5),
    ])
    def test_predict_same_value_as_pre_calculated(
        self, name, test_values, true_result
    ):
        model = self.models['Three features']
        prediction = model.predict(test_values)
        self.assertAlmostEqual(true_result, prediction.result)

    def test_predict_raises_ValueError_with_bad_number_of_feature_values(self):
        with self.assertRaises(ValueError):
            self.models['Two features'].predict(35)

    @unittest.expectedFailure
    def test_reversing_features_doesnt_change_prediction(self):
        pred = self.models['Two features'].predict([25, 130])
        pred_reverse = self.models['Two features reverse'].predict([130, 25])
        self.assertAlmostEqual(pred.result, pred_reverse.result)

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

    def __render_graph(self, model, name):
        import graphviz
        graph = graphviz.Source(model.export_graphviz())
        graph.render(name)


if __name__ == '__main__':
    unittest.main()
