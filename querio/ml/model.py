import collections
import operator
import sklearn
import sklearn.tree
import sklearn.model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from functools import reduce
import numpy as np
import pandas as pd
from .utils import *
from .prediction import Prediction


class Model:

    def __init__(self, data, feature_names, output_name, max_depth=None):
        self.feature_names = make_into_list_if_scalar(feature_names)
        self.output_name = output_name
        ## data = self.__preprocess_data__(data)

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

    def __preprocess_data__(self, data):
        le = LabelEncoder()
        ohe = OneHotEncoder()
        processed_data = data.copy()
        processed_feature_names = self.feature_names.copy()

        for col in data.columns:
            if (data[col].dtype == np.bool and col in self.feature_names):
                processed_data[col] = processed_data[col].astype(float)

        for col in data.columns:
            if (data[col].dtype in [np.object, np.str] and col in self.feature_names):
                processed_data[col] = le.fit_transform(processed_data[col])
                col_array = ohe.fit_transform(processed_data[col].values.reshape(-1, 1)).toarray() ## from 1D array to 2D
                new_col_names = [col + "_" + str(int(i)) for i in range(col_array.shape[1])]
                col_df = pd.DataFrame(col_array, columns = new_col_names)
                del processed_data[col]
                processed_data = pd.concat([processed_data, col_df], axis=1)
                processed_feature_names.remove(col)
                processed_feature_names += new_col_names

        self.feature_names = processed_feature_names
        return processed_data

    def predict(self, feature_values):
        """Returns a tuple with (mean, variance)"""
        feature_values = self._convert_to_dict(feature_values)
        leaf_set = reduce(operator.and_, [
            self._query_for_one_feature(name, value)
            for name, value in feature_values.items()
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

        result_tuple = calculate_mean_and_variance_from_populations(leaf_populations)
        return Prediction(result_tuple[0], result_tuple[1])

    def _convert_to_dict(self, feature_values):
        if not isinstance(feature_values, collections.Mapping):
            feature_values = make_into_list_if_scalar(feature_values)
            if len(feature_values) != len(self.feature_names):
                raise ValueError(
                    "When feature_values is not a dictionary, it's length " +
                    "must be the number of features."
                )
            feature_values = {
                self.feature_names[i]: feature_values[i]
                for i in range(0, len(feature_values))
            }
        return feature_values

    def _query_for_one_feature(self, feature_name, feature_value):
        """Returns a set of all tree node indexes that match the give
        value of the given feature"""
        feature_index = self.feature_names.index(feature_name)
        tree = self.tree.tree_
        return self.__recurse_tree_node(0, feature_index, feature_value)

    def __recurse_tree_node(self, node_index, feature_index, feature_value):
        tree = self.tree.tree_

        if self.__is_leaf_node(node_index):
            return {node_index}

        if tree.feature[node_index] == feature_index:
            if float(feature_value) <= tree.threshold[node_index]:
                next_node = tree.children_left[node_index]
            else:
                next_node = tree.children_right[node_index]
            return self.__recurse_tree_node(
                next_node, feature_index, feature_value
            )
        else:
            return self.__recurse_tree_node(
                tree.children_left[node_index], feature_index, feature_value
            ) | self.__recurse_tree_node(
                tree.children_right[node_index], feature_index, feature_value
            )

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
            feature_names=self.feature_names,
            filled=True, rounded=True,
            special_characters=True
        )
