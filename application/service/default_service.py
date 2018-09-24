import ml
import db


db_string = "postgres://otoihucuckhivv:7b93b9777ab13649dc0af7ef499a699a307c7ffd5ca1733389e1dfb1dac5253a@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/dab0467utv53cp"
model = ml.Model(db_string)

def get_example_from_db():
    return db.get_example_row_from_db()

def accuracy():
    return ['age', model.get_accuracy_score()]

def get_avg_single_param(param):
    return db.get_avg_one_param(param)

def get_avg_three_param(first, second, third):
    return db.get_avg_three_param(first, second, third)

def get_user_defined_query(first, second, third, fourth):
    return db.get_user_defined_query(first, second, third, fourth)

def get_population_variance(param):
    return db.get_population_variance_from_db(param)
