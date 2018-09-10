
def predict_income(age):
    return age * 10.5


def get_example_row_from_db():
    return {'age': 30, 'income': predict_income(30)}
