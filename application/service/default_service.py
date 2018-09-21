import ml
import db


def get_example_from_db():
    return db.get_example_row_from_db()

def accuracy():
    return ml.return_accuracy()

def get_avg_single_param(param):
    return db.get_avg_one_param(param)

def get_avg_three_param(first, second, third):
    return db.get_avg_three_param(first, second, third)

def get_user_defined_query(first, second, third, fourth):
    return db.get_user_defined_query(first, second, third, fourth)