import collections
import sys
import operator
import sklearn
import sklearn.tree
import sklearn.ensemble
import sklearn.model_selection
from functools import reduce
import numpy as np
import pandas as pd
from querio.ml.utils import *
from querio.ml.treetraversal import query_one_tree
from querio.ml.prediction import Prediction
from querio.ml.expression.feature import Feature
from querio.ml.expression.cond import Op
from querio.ml.expression.expression import Expression


class Model:
    """A decision tree regressor extension capable of more compex queries.

    Model uses a decision tree regressor as a foundation to predict
    the mean and variance for samples matching a compex query.

    Parameters:
    data: pandas.DataFrame
        The data that is queried. If the DataFrame was created with a pandas
        read-method with chunksize set, one decision tree is created for each
        chunk. Queries then return the mean result of all the query on all
        of the trees.
    feature_names: list of string
        The names of the columns in the data that are used to narrow down the
        rows.
    output_name: string
        The name of the column used to calculate the mean and the variance in
        queries.
    max_depth: int, optional
        A limit to the maximum depth of the underlying decision tree.

    Queries:
    The queries can contain conditions for equalities and inequalities
    between the features and constant real numbers. The conditions can be
    combined with arbitrarily nested or and and operation.

    Example queries:
    Feature('age') == 30 -- find the mean and the variance of all 30 year olds.
    (Feature('income') > 5000) & (Feature('age') == 40)
    (Feature('height') > 180) | ((Feature('age') < 50) & (Feature('age') > 40))
    """

    def __init__(self, data, feature_names, output_name, max_depth=None):
        """Initialize the Model."""
        feature_names = make_into_list_if_scalar(feature_names)
        self.output_name = output_name
        self.features = {}
        self.feature_names = feature_names
        self.model_feature_names = []
        self.test_scores = []
        self.train_scores = []
        if max_depth is None:
            self.max_depth = sys.getrecursionlimit()
        else:
            self.max_depth = max_depth

        self.trees = []

        self.feature_min_max_count = None
        if isinstance(data, pd.DataFrame):
            self.process_chunk(data)
        else:
            for i, chunk in enumerate(data):
                self.process_chunk(chunk)

    def process_chunk(self, chunk):
        def update_min_max_count_dict(key, dict1, dict2):
            return {
                'max': max(dict1[key]['max'], dict2[key]['max']),
                'min': max(dict1[key]['min'], dict2[key]['min']),
                'count': dict1[key]['count'] + dict2[key]['count'],
            }

        new_min_max_count = get_feature_min_max_count(
            chunk, self.feature_names
        )
        if self.feature_min_max_count is None:
            self.feature_min_max_count = new_min_max_count
        else:
            self.feature_min_max_count = {
                key: update_min_max_count_dict(
                    key, self.feature_min_max_count, new_min_max_count
                )
                for key in self.feature_names
            }
        chunk = self.__preprocess_data(chunk, self.feature_names)
        tree = sklearn.tree.DecisionTreeRegressor(
            criterion='mse',
            random_state=42,
            max_depth=min(self.max_depth, sys.getrecursionlimit() / 2 - 10),
        )
        train, test = sklearn.model_selection.train_test_split(
            chunk, random_state=42
        )
        tree.fit(train[self.model_feature_names], train[self.output_name])
        self.test_scores.append(tree.score(
            test[self.model_feature_names], test[self.output_name]
        ))
        self.train_scores.append(tree.score(
            train[self.model_feature_names], train[self.output_name]
        ))
        self.trees.append(tree)

    def __preprocess_data(self, data, feature_names):
        categorical_features = []
        data_columns = data.columns.copy()
        for col in data_columns:
            if data[col].dtype == np.bool and col in feature_names:
                data[col] = data[col].astype(float)
        for col in data_columns:
            if data[col].dtype == np.object and col in feature_names:
                data = pd.concat(
                    [data, pd.get_dummies(data[col], prefix=col)], axis=1
                )
                categorical_features.append(col)
        for feature in feature_names:
            col_dict = {"data_type": data[feature].dtype}
            if feature in categorical_features:
                sub_columns = []
                for sub in data.columns:
                    correct_prefix = sub.startswith(feature + "_")
                    if correct_prefix and sub not in feature_names:
                        sub_columns.append(sub)
                col_dict["columns"] = sub_columns
                self.model_feature_names += sub_columns
                data.drop(feature, axis=1, inplace=True)
            else:
                col_dict["columns"] = [feature]
                self.model_feature_names.append(feature)
            self.features[feature] = col_dict
        return data

    def query(self, expression):
        """Return the predicted mean and variance for the given condition

        Arguments:
        expression -- an Expression
        Returns:
        A Prediction object that contains the predicted mean and variance of
        samples matching the given conditions.
        """
        if not isinstance(expression, Expression):
            raise TypeError('expression must be an Expression')
        for condition in expression:
            if condition.feature not in [*self.features]:
                raise ValueError('{0} is not a feature name'.format(
                    condition.feature
                ))
            if isinstance(condition.threshold, bool):
                condition.threshold = float(condition.threshold)
            elif len(self.features[condition.feature]["columns"]) > 1:
                categories = self.get_categories_for_feature(condition.feature)
                if condition.threshold not in categories:
                    raise ValueError(
                        '{0} does not contain value \"{1}\"'.format(
                            condition.feature, condition.threshold
                        )
                    )
                condition.feature += "_" + condition.threshold
                condition.threshold = 1.0

        results = [
            query_one_tree(decision_tree, expression, self.model_feature_names)
            for decision_tree in self.trees
        ]
        mean = sum([result[0] for result in results]) / len(results)
        var = sum([result[1] for result in results]) / len(results)
        return Prediction(mean, var)

    def get_score_for_test(self):
        """Return the mean R^2 score of the decision trees on the test data."""
        return sum(self.test_scores) / len(self.test_scores)

    def get_score_for_train(self):
        """Return the mean R^2 score of the decision trees on the training data."""  # noqa
        return sum(self.train_scores) / len(self.train_scores)

    def export_graphviz(self):
        """Return a visualizations of the decision trees in graphviz format."""
        return [
            sklearn.tree.export_graphviz(
                tree, out_file=None,
                feature_names=self.model_feature_names,
                filled=True, rounded=True,
                special_characters=True
            )
            for tree in self.trees
        ]

    def _get_features(self):
        """Return a dict containing the type and columns of all features."""
        return self.features

    def get_feature_names(self):
        """Return the names of all the features."""
        return [*self.features]

    def get_categories_for_feature(self, feature_name):
        """Return the categories for a categorical feature."""
        categories = []
        if feature_name in [*self.features]:
            columns = self.features[feature_name]['columns']
            if len(columns) > 1:
                for col in columns:
                    categories.append(col.split(feature_name + "_", 1)[1])
            else:
                raise ValueError(
                    '{0} is not categorical.'.format(feature_name)
                )
        else:
            raise ValueError('{0} is not a feature.'.format(feature_name))
        return categories
