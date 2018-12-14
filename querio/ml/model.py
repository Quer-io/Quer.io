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
    model_params: dict, optional
        A keyword arguments dict used to pass arguments to the decision tree
        model. See Scikit Learn documentation on decision tree regressors for
        accepted parameters and theirs function.

    Queries:
    The queries can contain conditions for equalities and inequalities
    between the features and constant real numbers. The conditions can be
    combined with arbitrarily nested 'or' and 'and' operations.

    Example queries:
    Feature('age') == 30 -- find the mean and the variance of all 30 year olds.
    (Feature('income') > 5000) & (Feature('age') == 40)
    (Feature('height') > 180) | ((Feature('age') < 50) & (Feature('age') > 40))
    """

    def __init__(
        self, data, table_name, model_name, feature_names,
        output_name, db_path, model_params={}
    ):

        """Initialize the Model."""
        feature_names = make_into_set(feature_names)
        self.table_name = table_name
        self.model_name = model_name
        self.output_name = output_name
        self.features = {}
        self.feature_names = feature_names
        self.model_feature_names = []
        self.test_scores = []
        self.train_scores = []
        self.db_path = db_path
        self.model_params = model_params
        # if max_depth is None:
        #     self.max_depth = sys.getrecursionlimit()
        # else:
        #     self.max_depth = max_depth

        self.trees = []

        self.feature_min_max_count = None
        self.plot_data_frames = []
        if isinstance(data, pd.DataFrame):
            self.process_chunk(data)
        else:
            for chunk in data:
                self.process_chunk(chunk)
        self.plot_data = pd.concat(self.plot_data_frames, ignore_index=True)

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
            **self.model_params
        )
        train, test = sklearn.model_selection.train_test_split(
            chunk, random_state=42
        )
        plot, _ = sklearn.model_selection.train_test_split(
            chunk, random_state=42,
            train_size=min(100, len(chunk) - 1), test_size=0
        )
        self.plot_data_frames.append(plot)
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
        """Return the predicted mean and variance for the given condition.

        Arguments:
        expression -- an Expression
        Returns:
        A Prediction object that contains the predicted mean and variance of
        samples matching the given conditions.
        Throws:
        NoMatch when no rows match the expression.
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
            query_one_tree(
                decision_tree, expression, self.model_feature_names,
                self.feature_min_max_count
            )
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

    def visualize_decision(
        self, feature, axis, expression=None,
        prediction_style='b-', actual_style='r.',
        query_points=100, param_dict={}
    ):
        """Plot the prediction with some real data points.

        Plots query(Feature(feature) == x) for points in the range of the
        feature. Also plots 100 points per chunk of actual data passed to
        the Model constructor. By default the prediction is plotted with a
        blue line and the actual points are plotted as red dots. It's
        recommended to plot the actual points with points, as their order
        in the dataset is arbitrary.

        Parameters:
        feature: str
            The feature to plot.
        axis: matplotlib.axes.Axes object
            The axis object the plot is made to.
        expression: Expression
            An expression limiting the query range. Only query points and
            actual points that match the expression are plotted. If the
            expression is very restrictive compared to the range of the
            plotted feature, ensure that query_points is set high enough to
            get an appropriate number of points in the plot.
        prediction_style: str
            The style of the prediction. Default blue line (b-)
        actual_style: str
            The style of the actual points. Default red dot (r.)
        query_points: int
            The number of points the model is queried at. Default 100
        param_dict:
            Extra arguments passed to the axis object for plotting.

        Example:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        model.visualize_decision('age', ax)
        fig.show()
        """
        min_max = self.feature_min_max_count[feature]
        min = min_max['min']
        max = min_max['max']
        xs = np.linspace(min, max, query_points)
        if expression is not None:
            xs = [x for x in xs if expression.match(feature, x)]
            matching_rows = self.plot_data[
                self.plot_data.apply(
                    lambda row: expression.match(feature, row[feature]),
                    axis=1
                )
            ]
        else:
            matching_rows = self.plot_data
        axis.plot(
            xs, [self.query(Feature(feature) == x).result for x in xs],
            prediction_style, **param_dict
        )
        axis.plot(
            matching_rows[feature], matching_rows[self.output_name],
            actual_style, **param_dict
        )

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
