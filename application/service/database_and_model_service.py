import ml
import db
from db.data_accessor import DataAccessor

class DatabaseAndModelService:

    def __init__(self, predicting_column_name, predicted_column_name, db_connection):
        self.db = DataAccessor(db_connection[0], db_connection[1])
        self.predicting_column_name = predicting_column_name
        self.predicted_column_name = predicted_column_name
        self.get_null_value()
        if self.db.connected:
            self.model = ml.Model(self.db.get_all_data(), self.predicted_column_name, self.predicting_column_name)

    def get_prediction_for_value(self, value):
        return self.model.predict(value)

    def get_example_from_db(self):
        return self.db.get_example_row_from_db()

    def get_accuracy(self):
        return [self.predicted_column_name, self.model.get_score_for_train()]

    def get_accuracy_for_test(self):
        return [self.predicted_column_name, self.model.get_score_for_test()]

    def get_user_defined_query(self, function, column, where, like):
        return self.db.get_user_defined_query(function, column, where, like)

    def get_population_variance(self, column):
        return self.db.get_population_variance_from_db(column)

    def get_filtered_variance(self, column, where, like):
        return self.db.get_variance_from_filtered_rs(column, where, like)

    def get_filtered_resultset(self, where, like):
        return self.db.get_filtered_resultset(where, like)

    def get_column_names_from_db(self):
        #TODO: When DB contains more than one table, a table name needs to be passed as an argument to the db module
        return self.db.get_table_column_names()

    def get_null_value(self):
        return self.get_null_value
