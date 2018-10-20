import collections
import sys
import operator
import sklearn
import sklearn.tree
import sklearn.model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from functools import reduce
import numpy as np
import pandas as pd
from querio.ml.utils import *
from querio.ml.prediction import Prediction
from querio.ml.feature import Feature
from querio.ml.cond import Op


class Model:

    def __init__(self, data, feature_names, output_name, max_depth=None):
        self.feature_names = make_into_list_if_scalar(feature_names)
        self.output_name = output_name
        self.feature_min_max_count = get_feature_min_max_count(data, self.feature_names)
        if max_depth is None:
            max_depth = sys.getrecursionlimit()
        ## data = self.__preprocess_data__(data)

        self.tree = sklearn.tree.DecisionTreeRegressor(
            criterion='mse',
            random_state=42,
            max_depth=min(max_depth, sys.getrecursionlimit() / 2 - 10)
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

    def predict(self, conditions):
        for condition in conditions:
            if condition.feature not in self.feature_names:
                raise ValueError('{0} is not a feature name'.format(
                    condition.feature
                ))

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
        feature_index = self.feature_names.index(condition.feature)
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
            feature_names=self.feature_names,
            filled=True, rounded=True,
            special_characters=True
        )
