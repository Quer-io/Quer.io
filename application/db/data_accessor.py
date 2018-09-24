import sqlalchemy
from sqlalchemy import exc

db_string = "postgres://otoihucuckhivv:7b93b9777ab13649dc0af7ef499a699a307c7ffd5ca1733389e1dfb1dac5253a@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/dab0467utv53cp"

# represents the core interface to the database
engine = sqlalchemy.create_engine(db_string)
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


def get_avg_one_param(avg):
    check_avg = conn.execute("SELECT {} FROM person limit 1".format(avg))
    avg_column = check_avg.fetchone()
    if type(avg_column[0]) is int:
        result = conn.execute("SELECT avg({}) FROM person".format(avg))
        value = result.fetchone()
    else:
        return "Bad parameter type - column type has to be int!"
    return value[0]


def get_avg_three_param(avg, where, like):
    check_avg = conn.execute("SELECT {} FROM person limit 1".format(avg))
    check_where = conn.execute("SELECT {} FROM person limit 1".format(where))
    avg_column = check_avg.fetchone()
    where_column = check_where.fetchone()

    if type(avg_column[0]) is int:
        if type(where_column[0]) is int:
            result = conn.execute("SELECT avg({}) FROM person WHERE {} = {}".format(avg, where, like))
            value = result.fetchone()
        else:
            result = conn.execute("SELECT avg({}) FROM person WHERE {} LIKE '{}'".format(avg, where, like))
            value = result.fetchone()
    else:
        return "Bad parameter type - column type has to be int!"
    return value[0]


def get_count_with_param(count, where, like):
    if type(like) is int:
        result = conn.execute("SELECT count({}) FROM person WHERE {} = {}".format(count, where, like))
    else:
        result = conn.execute("SELECT count({}) FROM person WHERE {} LIKE '{}'".format(count, where, like))
    return result


def get_user_defined_query(function, column, where, like):
    try:
        check_column = conn.execute("SELECT {} FROM person limit 1".format(column))
        check_where = conn.execute("SELECT {} FROM person limit 1".format(where))
        avg_column = check_column.fetchone()
        where_column = check_where.fetchone()

        if function.lower() == 'avg':
            if type(avg_column[0]) is int:
                if type(where_column[0]) is int:
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

        return value[0]
    except exc.SQLAlchemyError:
        print("Something went wrong! Encountered SQLAlchemyError!")


def get_population_variance_from_db(column):
    result = conn.execute("SELECT var_pop({}) FROM person".format(column))
    value = result.fetchone()
    return value[0]
