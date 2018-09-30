import ml
import db

db_string = "postgres://otoihucuckhivv:7b93b9777ab13649dc0af7ef499a699a307c7ffd5ca1733389e1dfb1dac5253a@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/dab0467utv53cp"
model = ml.Model(db_string)


def get_example_from_db():
    return db.get_example_row_from_db()


def accuracy():
    return ['age', model.get_accuracy_score()]

def get_user_defined_query(function, column, where, like):
    return db.get_user_defined_query(function, column, where, like)

def get_population_variance(param):
    return db.get_population_variance_from_db(param)

def get_filtered_resultset(where, like):
    return db.get_filtered_resultset(where, like)
    
def get_column_names_from_db():
    #TODO: When DB contains more than one table, a table name needs to be passed as an argument to the db module
    return db.get_table_column_names()


