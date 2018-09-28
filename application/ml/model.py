import sklearn
import sklearn.tree
import sklearn.model_selection


class Model:
    def __init__(self, data, feature_name, output_name):
        self.feature_name = feature_name
        self.output_name = output_name
        self.tree = sklearn.tree.DecisionTreeRegressor(
            criterion='mse',
            random_state=42
        )
        train, test = sklearn.model_selection.train_test_split(
            data, random_state=42
        )
        self.tree.fit(train[[self.feature_name]], train[self.output_name])
        self.test_score = self.tree.score(
            test[[self.feature_name]], test[self.output_name]
        )
        self.train_score = self.tree.score(
            train[[self.feature_name]], train[self.output_name]
        )

    def predict(self, feature_value):
        """Returns a tuple with (mean, variance)"""
        node_index = self.tree.apply([[feature_value]])[0]
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
