import unittest
import pandas as pd
import numpy as np
from parameterized import parameterized
import os.path

from querio.ml import Model
from querio.ml import NoMatch
from querio.ml.expression.cond import Cond
from querio.ml.expression.cond import Op
from querio.ml.expression.feature import Feature
from querio.ml.expression.expressionnode import BoolOp
from querio.ml.expression.expressionnode import ExpressionTreeNode


class ModelTest(unittest.TestCase):

    def setUp(self):
        ages = [22, 44, 36, 64, 32, 86, 11, 45]
        incomes = [age * 301 for age in ages]
        heights = [age * 50 for age in ages]
        github_stars = [age * 20 + 10 for age in ages]
        professions = [
            'accountant', 'janitor', 'president', 'janitor',
            'accountant', 'programmer', 'janitor', 'account_manager'
        ]
        is_client = [True, True, False, True, False, False, False, True]
        self.data = pd.DataFrame({
            'age': ages, 'income': incomes, 'height': heights,
            'github_stars': github_stars, 'profession': professions,
            'is_client': is_client, 'prof_with_underscore': professions
        })
        self.models = {
            'One feature': Model(self.data, 'table', "", 'age', 'income', ''),
            'One feature with boolean': Model(
                self.data, 'table', "", 'is_client', 'income', ''
            ),
            'One feature with categorical': Model(
                self.data, 'table', "", 'profession', 'income', ''
            ),
            'One feature with categorical_underscore': Model(
                self.data, 'table', "", 'prof_with_underscore', 'income', ''
            ),
            'Two features with categorical': Model(
                self.data, 'table', "", ['age', 'profession'], 'income', ''
            ),
            'Two features': Model(
                self.data, 'table', "", ['age', 'height'], 'income', ''
            ),
            'Two features reverse': Model(
                self.data, 'table', "", ['height', 'age'], 'income', ''
            ),
            'Three features': Model(
                self.data, 'table', "", ['age', 'height', 'github_stars'],
                'income', ''
            )
        }

    @parameterized.expand([
        ('One feature', Cond('age', Op.eq, 35)),
        ('One feature with boolean', Cond('is_client', Op.eq, True)),
        ('One feature with boolean', Feature('is_client') == 1),
        ('One feature with categorical', Cond('profession', Op.eq, 'janitor')),
        ('One feature with categorical_underscore', (
            Feature('prof_with_underscore') == 'janitor'
        )),
        ('One feature with categorical_underscore', (
            Feature('prof_with_underscore') == 'account_manager'
        )),
        ('One feature with categorical', Feature('profession') == 'janitor'),
        ('Two features', ExpressionTreeNode(
            Cond('age', Op.eq, 35), BoolOp.and_, Cond('height', Op.eq, 700)
        )),
        ('Two features', (Feature('age') == 20) & (Feature('height') == 800)),
        ('Two features', (Feature('age') == 20) | (Feature('height') == 800)),
        ('Three features', (
            ((Feature('age') == 20) | (Feature('height') == 800))
            & (Feature('github_stars') == 300)
        )),
    ])
    def test_query_gives_value_in_correct_range(self, name, test_conditions):
        prediction = self.models[name].query(
            test_conditions
        )
        self.assertGreaterEqual(prediction.result, self.data['income'].min())
        self.assertLessEqual(prediction.result, self.data['income'].max())
        self.assertGreaterEqual(prediction.variance, 0)

    @parameterized.expand([
        ('One feature', Cond('age', Op.eq, 40)),
        ('Two features', ExpressionTreeNode(
            Cond('age', Op.eq, 41), BoolOp.and_, Cond('height', Op.eq, 134)
        ))
    ])
    @unittest.skip
    def test_query_same_mean_as_sklearn_predict(self, name, test_condition):
        model = self.models[name]
        prediction = model.query(test_condition)
        self.assertAlmostEqual(
            model.tree.predict([[
                cond.threshold for cond in test_condition
            ]])[0],
            prediction.result
        )

    @parameterized.expand([
        ('Too old', Feature('age') > 100),
        ('Contradiction', (
            (Feature('height') > 1000) & (Feature('height') < 900)
        )),
        ('Too few github stars', Feature('github_stars') == 100)
    ])
    def test_query_raises_NoMatch_when_no_rows_match(
        self, name, test_condition
    ):
        with self.assertRaises(NoMatch):
            model = self.models['Three features']
            model.query(test_condition)

    def test_query_raises_ValueError_with_bad_feature_names(self):
        with self.assertRaises(ValueError):
            self.models['Two features'].query(
                Cond('github_stars', Op.eq, 0)
            )

    def test_query_raises_ValueError_with_bad_categorical_feature_values(self):
        with self.assertRaises(ValueError):
            self.models['One feature with categorical'].query(
                Cond('profession', Op.eq, 'firefighter')
            )

    @unittest.expectedFailure
    def test_reversing_features_doesnt_change_prediction(self):
        pred = self.models['Two features'].query([25, 130])
        pred_reverse = self.models['Two features reverse'].query([130, 25])
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

    def test_loading_by_chunk(self):
        data = pd.read_csv(
            os.path.join(os.path.dirname(__file__), '1000.csv'), chunksize=100
        )
        model = Model(data, 'table', "", ['age', 'height'], 'income', '')
        pred = model.query(Feature('age') > 20)
        self.assertEqual(len(model.trees), 10)
        self.assertEqual(len(model.plot_data), 990)

    @parameterized.expand([
        ('Two features with categorical', 'profession'),
        ('One feature with categorical_underscore', 'prof_with_underscore')
    ])
    def test_get_categories_for_feature_returns_categories(self, model, feat):
        model = self.models[model]
        categories = model.get_categories_for_feature(feat)
        true_categories = [
            'accountant', 'janitor', 'president',
            'programmer', 'account_manager'
        ]
        true_categories.sort()
        categories.sort()
        self.assertEqual(categories, true_categories)

    @parameterized.expand([
        ('age'),
        ('income'),
        ('not_feature')
    ])
    def test_get_categories_for_feature_raises_with_not_categorical(
        self, feature
    ):
        model = self.models['Two features with categorical']
        with self.assertRaises(ValueError):
            model.get_categories_for_feature(feature)

    def __render_graph(self, model, name):
        import graphviz
        graph = graphviz.Source(model.export_graphviz())
        graph.render(name)


if __name__ == '__main__':
    unittest.main()
