import unittest
import pandas as pd
import numpy as np
from parameterized import parameterized

from querio.ml import Model
from querio.ml.cond import Cond
from querio.ml.cond import Op
from querio.ml.feature import Feature
from querio.ml.utils import make_into_list_if_scalar


class ModelTest(unittest.TestCase):

    def setUp(self):
        ages = [22, 44, 36, 64, 32, 86, 11, 45]
        incomes = [age * 301 for age in ages]
        heights = [age * 50 for age in ages]
        github_stars = [age * 20 + 10 for age in ages]
        professions = [
            'accountant', 'janitor', 'president', 'janitor', 
            'accountant', 'programmer', 'janitor', 'programmer'
        ]
        is_client = [True, True, False, True, False, False, False, True]
        self.data = pd.DataFrame({
            'age': ages, 'income': incomes, 'height': heights,
            'github_stars': github_stars, 'profession': professions,
            'is_client': is_client
        })
        self.models = {
            'One feature': Model(self.data, 'age', 'income'),
            'One feature with boolean': Model(self.data, 'is_client', 'income'),
            'One feature with categorical': Model(self.data, 'profession', 'income'),
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
        ('One feature', [Cond('age', Op.eq, 35)]),
        ('One feature with boolean', [Cond('is_client', Op.eq, True)]),
        ('One feature with categorical', [Cond('profession', Op.eq, 'janitor')]),
        ('Two features', [Cond('age', Op.eq, 35), Cond('height', Op.eq, 120)]),
    ])
    def test_predict_gives_value_in_correct_range(self, name, test_conditions):
        prediction = self.models[name].predict(
            test_conditions
        )
        self.assertGreaterEqual(prediction.result, self.data['income'].min())
        self.assertLessEqual(prediction.result, self.data['income'].max())
        self.assertGreaterEqual(prediction.variance, 0)

    @parameterized.expand([
        ('One feature', [Cond('age', Op.eq, 40)]),
        ('Two features', [Cond('age', Op.eq, 41), Cond('height', Op.eq, 134)])
    ])
    def test_predict_same_mean_as_sklearn_predict(self, name, test_conditions):
        model = self.models[name]
        prediction = model.predict(test_conditions)
        self.assertAlmostEqual(
            model.tree.predict([[
                cond.threshold for cond in test_conditions
            ]])[0],
            prediction.result
        )

    @parameterized.expand([
        ('1', [Cond('age', Op.eq, 42)], 10535),
        ('2', [Cond('age', Op.eq, 33), Cond('height', Op.eq, 100)],
            7926.333333333333333),
        ('3', [Cond('height', Op.eq, 120), Cond('github_stars', Op.eq, 54)],
            3311),
        ('4', [Cond('github_stars', Op.eq, 42)], 10685.5),
        ('5', [Feature('age') == 42], 10535),
        ('6', [Feature('height') > 2500], 16404.5),
        ('7', [Feature('github_stars') > 700], 14548.333333333333333333),
        ('8', [Feature('age') > 40], 10535),
        ('9', [Feature('height') < 1000, Feature('github_stars') > 700],
            10836),
    ])
    def test_predict_same_value_as_pre_calculated(
        self, name, test_conditions, true_result
    ):
        model = self.models['Three features']
        prediction = model.predict(test_conditions)
        self.assertAlmostEqual(true_result, prediction.result)

    def test_predict_raises_ValueError_with_bad_feature_names(self):
        with self.assertRaises(ValueError):
            self.models['Two features'].predict(
                [Cond('github_stars', Op.eq, 0)]
            )

    def test_predict_raises_ValueError_with_bad_categorical_feature_values(self):
        with self.assertRaises(ValueError):
            self.models['One feature with categorical'].predict(
                [Cond('profession', Op.eq, 'firefighter')]
            )

    @unittest.expectedFailure
    def test_reversing_features_doesnt_change_prediction(self):
        pred = self.models['Two features'].predict([25, 130])
        pred_reverse = self.models['Two features reverse'].predict([130, 25])
        self.assertAlmostEqual(pred.result, pred_reverse.result)

    @parameterized.expand([
        ('One feature'),
        ('Two features'),
        ('Three features'),
    ])
    def test_train_score_is_sensible(self, name):
        score = self.models[name].get_score_for_train()
        self.assertLessEqual(score, 1)

    @parameterized.expand([
        ('One feature'),
        ('Two features'),
        ('Three features'),
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
