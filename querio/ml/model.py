import collections
import sys
import operator
import sklearn
import sklearn.tree
import sklearn.model_selection
from functools import reduce
import numpy as np
import pandas as pd
from querio.ml.utils import *
from querio.ml.prediction import Prediction
from querio.ml.feature import Feature
from querio.ml.cond import Op


class Model:

    def __init__(self, data, feature_names, output_name, max_depth=None):
        feature_names = make_into_list_if_scalar(feature_names)
        self.output_name = output_name
        self.features = {}
        self.model_feature_names = []
        self.feature_min_max_count = get_feature_min_max_count(
            data, feature_names
        )
        data = self.__preprocess_data__(data, feature_names)
        if max_depth is None:
            max_depth = sys.getrecursionlimit()

        self.tree = sklearn.tree.DecisionTreeRegressor(
            criterion='mse',
            random_state=42,
            max_depth=min(max_depth, sys.getrecursionlimit() / 2 - 10)
        )

        train, test = sklearn.model_selection.train_test_split(
            data, random_state=42
        )
        self.tree.fit(train[self.model_feature_names], train[self.output_name])
        self.test_score = self.tree.score(
            test[self.model_feature_names], test[self.output_name]
        )
        self.train_score = self.tree.score(
            train[self.model_feature_names], train[self.output_name]
        )

    def __preprocess_data__(self, data, feature_names):
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

    def predict(self, conditions):
        if not isinstance(conditions, list):
            raise TypeError('Conditions must be a list of Condition')
        for condition in conditions:
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

        leaf_set = reduce(operator.and_, [
            self._query_for_one_condition(cond)
            for cond in conditions
        ])
        tree = self.tree.tree_
        leaf_populations = [
            Population(
                tree.n_node_samples[leaf],
                tree.value[leaf][0][0],
                tree.impurity[leaf]
            )
            for leaf in leaf_set
        ]

        result_tuple = calculate_mean_and_variance_from_populations(
            leaf_populations
        )
        return Prediction(result_tuple[0], result_tuple[1])

    def _query_for_one_condition(self, condition):
        """Returns a set of all tree node indexes that match the given
        value of the given feature"""
        feature_index = self.model_feature_names.index(condition.feature)
        tree = self.tree.tree_
        return self.__recurse_tree_node(
            0, feature_index, condition.op, float(condition.threshold)
        )

    def __recurse_tree_node(self, node_index, feature_index, op, threshold):
        def recurse_both_children():
            return self.__recurse_tree_node(
                tree.children_left[node_index], feature_index, op, threshold
            ) | self.__recurse_tree_node(
                tree.children_right[node_index], feature_index, op, threshold
            )

        def recurse_right_child():
            return self.__recurse_tree_node(
                tree.children_right[node_index], feature_index, op, threshold
            )

        def recurse_left_child():
            return self.__recurse_tree_node(
                tree.children_left[node_index], feature_index, op, threshold
            )

        tree = self.tree.tree_

        if self.__is_leaf_node(node_index):
            return {node_index}

        if tree.feature[node_index] == feature_index:
            if op is Op.eq:
                if threshold <= tree.threshold[node_index]:
                    return recurse_left_child()
                else:
                    return recurse_right_child()
            elif op is Op.lt:
                if threshold <= tree.threshold[node_index]:
                    return recurse_left_child()
                else:
                    return recurse_both_children()
            elif op is Op.gt:
                if threshold < tree.threshold[node_index]:
                    return recurse_both_children()
                else:
                    return recurse_right_child()
            else:
                raise NotImplementedError(
                    'Unimplemented comparison {0}'.format(op)
                )
        else:
            return recurse_both_children()

    def __is_leaf_node(self, node_index):
        tree = self.tree.tree_
        return tree.children_left[node_index] == sklearn.tree._tree.TREE_LEAF

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
            feature_names=self.model_feature_names,
            filled=True, rounded=True,
            special_characters=True
        )

    def get_features(self):
        return self.features

    def get_feature_names(self):
        return [*self.features]

    def get_categories_for_feature(self, feature_name):
        categories = []
        if feature_name in [*self.features]:
            for col in self.features[feature_name]["columns"]:
                categories.append(col.split(feature_name + "_", 1)[1])
        return categories
