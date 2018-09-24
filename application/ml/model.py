import sklearn
import sklearn.tree
import sklearn.model_selection

# Should be removed when data is fetched from db module
import sqlalchemy
import pandas as pd


class Model:
    def __init__(self, db_string):
        self.tree = sklearn.tree.DecisionTreeRegressor(
            criterion='mse',
            random_state=42
        )
        engine = sqlalchemy.create_engine(db_string)
        data = pd.read_sql('SELECT * FROM person', engine)
        train, test = sklearn.model_selection.train_test_split(
            data, random_state=42
        )
        self.tree.fit(train[['age']], train['income'])
        self.accuracy_score = self.tree.score(test[['age']], test['income'])

    def predict(self, age):
        """Returns a tuple with (mean, variance)"""
        node_index = self.tree.apply([[age]])[0]
        return (
            self.tree.tree_.value[node_index][0][0],
            self.tree.tree_.impurity[node_index]
        )

    def get_accuracy_score(self):
        """Returns the R^2 accuracy score of the ML model on the test data."""
        return self.accuracy_score
