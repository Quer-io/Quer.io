import sqlalchemy
from sqlalchemy import exc
import math
import configparser
import os
import pandas as pd

APP_ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
APP_STATIC = os.path.join(APP_ROOT, 'configuration.ini')
config = configparser.ConfigParser()
config.read(APP_STATIC)
db_address = config['ORIG_DB']['db_address']

# represents the core interface to the database
engine = sqlalchemy.create_engine(db_address)
conn = engine.connect()
md = sqlalchemy.MetaData()

table = sqlalchemy.Table('person', md, autoload_with=engine)


def get_example_row_from_db():
    """Gets the first row of the database and return it as a dictionary.

    The keys of the dictionary are the column names of the database table,
    the values are the values of the table corresponding to the columns.
    """

    column_names = get_table_column_names()
    result = conn.execute("SELECT * FROM person").fetchone()
    return {column_name: result[column_name] for column_name in column_names}


def get_table_column_names():
    return table.columns.keys()

def get_filtered_resultset(where, like):
    try:
        check_where = conn.execute("SELECT {} FROM person limit 1".format(where))
        where_column = check_where.fetchone()

        if type(where_column[0]) is int:
            result = conn.execute("SELECT * FROM person WHERE {} = {}".format(where, like))
        else:
            result = conn.execute("SELECT * FROM person WHERE {} like '{}'".format(where, like))

        rs = result.fetchall()
        print(rs)
        return rs
    except exc.SQLAlchemyError as e:
        print("Something went wrong!")
        print(e)

def get_user_defined_query(function, column, where, like):
    try:
        check_column = conn.execute("SELECT {} FROM person limit 1".format(column))
        check_where = conn.execute("SELECT {} FROM person limit 1".format(where))
        avg_column = check_column.fetchone()
        where_column = check_where.fetchone()

        if function.lower() == 'avg':
            if type(avg_column[0]) is int:
                if type(where_column[0]) is int:
                    print("SELECT avg({}) FROM person WHERE {} = {}".format(column, where, like))
                    result = conn.execute("SELECT avg({}) FROM person WHERE {} = {}".format(column, where, like))
                    value = result.fetchone()
                else:
                    result = conn.execute("SELECT avg({}) FROM person WHERE {} like '{}'".format(column, where, like))
                    value = result.fetchone()
            else:
                return "Bad parameter type - column has to be int!"
        elif function.lower() == 'count':
            if type(like) is int:
                result = conn.execute("SELECT count({}) FROM person WHERE {} = {}".format(column, where, like))
                value = result.fetchone()
            else:
                result = conn.execute("SELECT count({}) FROM person WHERE {} like '{}'".format(column, where, like))
                value = result.fetchone()
        else:
            return "Unknown function - please choose from 'avg' or 'count'!"
        floor = math.floor(value[0])
        return floor
    except exc.SQLAlchemyError as e:
        print("Something went wrong!")
        print(e)


def get_population_variance_from_db(column):
    result = conn.execute("SELECT var_pop({}) FROM person".format(column))
    value = result.fetchone()
    return value[0]


def get_all_data():
    return pd.read_sql('SELECT * FROM person', engine)
