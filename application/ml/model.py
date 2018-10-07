import sklearn
import sklearn.tree
import sklearn.model_selection
import numpy as np
from .utils import make_into_list_if_scalar


class Model:
    def __init__(self, data, feature_names, output_name, max_depth=None):

        self.feature_names = make_into_list_if_scalar(feature_names)
        self.output_name = output_name
        self.tree = sklearn.tree.DecisionTreeRegressor(
            criterion='mse',
            random_state=42,
            max_depth=max_depth
        )
        train, test = sklearn.model_selection.train_test_split(
            data, random_state=42
        )
        self.tree.fit(train[self.feature_names], train[self.output_name])
        self.test_score = self.tree.score(
            test[self.feature_names], test[self.output_name]
        )
        self.train_score = self.tree.score(
            train[self.feature_names], train[self.output_name]
        )

    def predict(self, feature_values):
        """Returns a tuple with (mean, variance)"""
        feature_values = make_into_list_if_scalar(feature_values)
        node_index = self.tree.apply([feature_values])[0]
        return (
            self.tree.tree_.value[node_index][0][0],
            self.tree.tree_.impurity[node_index]
        )

    def get_score_for_test(self):
        """Returns the R^2 accuracy score of the ML model on the test data."""
        return self.test_score

    def get_score_for_train(self):
        """Returns the R^2 accuracy score of the ML model on the training
        data."""
        return self.train_score

    def export_graphviz(self):
        return sklearn.tree.export_graphviz(
            self.tree, out_file=None,
            feature_names=self.feature_names,
            filled=True, rounded=True,
            special_characters=True
        )
