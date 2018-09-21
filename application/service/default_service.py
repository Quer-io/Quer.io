import ml
import db


def get_example_from_db():
    return db.get_example_row_from_db()


def predict(age):
    return ml.predict_income(age)

def accuracy():
    return ml.return_accuracy()