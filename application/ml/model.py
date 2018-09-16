from sqlalchemy import create_engine

db_string = "postgres://otoihucuckhivv:7b93b9777ab13649dc0af7ef499a699a307c7ffd5ca1733389e1dfb1dac5253a@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/dab0467utv53cp"

# represents the core interface to the database
engine = create_engine(db_string)

conn = engine.connect()

def predict_income(age):
    return age * 10.5


def get_example_row_from_db():
    """Gets the first row of the database and return it as a dictionary.

    The keys of the dictionary are the column names of the database table,
    the values are the values of the table corresponding to the columns.
    """

    result = conn.execute("SELECT * FROM person").fetchone()

    return result
    # return {'age': 30, 'income': predict_income(30)}
