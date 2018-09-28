import ml
import db

model = ml.Model(db.get_all_data(), 'age', 'income')


def get_example_from_db():
    return db.get_example_row_from_db()


def accuracy():
    return ['age', model.get_score_for_test()]

def get_user_defined_query(function, column, where, like):
    return db.get_user_defined_query(function, column, where, like)


def get_population_variance(param):
    return db.get_population_variance_from_db(param)
