import sklearn
import sklearn.tree
import sklearn.model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd
from .utils import make_into_list_if_scalar


class Model:
    
    def __init__(self, data, feature_names, output_name, max_depth=None):       
        self.feature_names = make_into_list_if_scalar(feature_names)
        self.output_name = output_name
        self.data = data
        self.__preprocess_data__()

        self.tree = sklearn.tree.DecisionTreeRegressor(
            criterion='mse',
            random_state=42,
            max_depth=max_depth
        )

        train, test = sklearn.model_selection.train_test_split(
            self.data, random_state=42
        )

        self.tree.fit(train[self.feature_names], train[self.output_name])
        self.test_score = self.tree.score(
            test[self.feature_names], test[self.output_name]
        )
        self.train_score = self.tree.score(
            train[self.feature_names], train[self.output_name]
        )

    def __preprocess_data__(self):
        le = LabelEncoder()
        ohe = OneHotEncoder()
        processed_data = self.data.copy()
        processed_feature_names = self.feature_names.copy()

        for col in self.data.columns:
            if (self.data[col].dtype == np.bool and col in self.feature_names):
                processed_data[col] = processed_data[col].astype(float)

        for col in self.data.columns:
            if (self.data[col].dtype in [np.object, np.str] and col in self.feature_names):
                processed_data[col] = le.fit_transform(processed_data[col])
                col_array = ohe.fit_transform(processed_data[col].values.reshape(-1, 1)).toarray() ## from 1D array to 2D
                new_col_names = [col + "_" + str(int(i)) for i in range(col_array.shape[1])]
                col_df = pd.DataFrame(col_array, columns = new_col_names) 
                del processed_data[col]
                processed_data = pd.concat([processed_data, col_df], axis=1)
                processed_feature_names.remove(col)
                processed_feature_names += new_col_names

        self.feature_names = processed_feature_names
        self.data = processed_data.reindex(processed_feature_names.append(self.output_name))

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
