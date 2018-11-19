import unittest
import sklearn.tree
import pandas as pd
from parameterized import parameterized
from querio.ml.treetraversal import query_one_tree
from querio.ml.expression.cond import Cond
from querio.ml.expression.cond import Op
from querio.ml.expression.feature import Feature
from querio.ml.expression.expressionnode import BoolOp
from querio.ml.expression.expressionnode import ExpressionTreeNode


class TreeTraversalTest(unittest.TestCase):

    def setUp(self):
        ages = [22, 44, 36, 64, 32, 86, 11, 45]
        incomes = [age * 301 for age in ages]
        heights = [age * 50 for age in ages]
        github_stars = [age * 20 + 10 for age in ages]
        self.data = pd.DataFrame({
            'age': ages, 'income': incomes, 'height': heights,
            'github_stars': github_stars
        })
        self.tree = sklearn.tree.DecisionTreeRegressor(
            criterion='mse',
            random_state=42,
        )
        self.feature_names = ['age', 'height', 'github_stars']
        train, test = sklearn.model_selection.train_test_split(
            self.data, random_state=42
        )
        self.tree.fit(train[self.feature_names], train['income'])

    @parameterized.expand([
        ('1', Cond('age', Op.eq, 42), 10535),
        ('2', ExpressionTreeNode(
            Cond('age', Op.eq, 33), BoolOp.and_, Cond('height', Op.eq, 100)
        ), 7926.333333333333333),
        ('3', ExpressionTreeNode(
            Cond('height', Op.eq, 120), BoolOp.and_,
            Cond('github_stars', Op.eq, 54)
        ), 3311),
        ('4', Cond('github_stars', Op.eq, 42), 10685.5),
        ('5', Feature('age') == 42, 10535),
        ('6', Feature('height') > 2500, 16404.5),
        ('7', Feature('github_stars') > 700, 14548.333333333333333333),
        ('8', Feature('age') > 40, 10535),
        ('9', ExpressionTreeNode(
            Feature('height') < 1000, BoolOp.and_,
            Feature('github_stars') > 700
        ), 10836),
        ('10', (
            (Feature('height') == 1000) | (Feature('github_stars') == 100)
        ), 10535),
        ('11', (Feature('github_stars') == 100) | (
                (Feature('github_stars') == 700) & (Feature('height') == 1500)
        ), 10715.6),
    ])
    def test_query_same_value_as_pre_calculated(
        self, name, test_conditions, true_result
    ):
        prediction = query_one_tree(
            self.tree, test_conditions, self.feature_names
        )
        self.assertAlmostEqual(true_result, prediction[0])

    def __render_graph(self, tree, name):
        import graphviz
        grapviz = sklearn.tree.export_graphviz(
            self.tree, out_file=None,
            feature_names=self.feature_names,
            filled=True, rounded=True,
            special_characters=True
        )
        graph = graphviz.Source(grapviz)
        graph.render(name)
