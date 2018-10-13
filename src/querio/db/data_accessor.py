import sqlalchemy
import psycopg2
from sqlalchemy import exc
import math
import configparser
import os
import pandas as pd
import sys


class DataAccessor():

    def __init__(self, use_config_file, address):


        if use_config_file:
            self.get_db_address_from_file()
        else:
            self.db_address = address

        # represents the core interface to the database
        

        try:
            self.engine = sqlalchemy.create_engine(self.db_address)
            self.conn = self.engine.connect()
            self.md = sqlalchemy.MetaData()
            self.table = sqlalchemy.Table('person', self.md, autoload_with=self.engine)
            self.connected = True
            print("Connection established")
        except exc.OperationalError as e:
            print("Invalid database settings. No connection to database")
            self.connected = False
            return
        
        




    def get_db_address_from_file(self):
        if getattr(sys, 'frozen', False):
            APP_STATIC = os.path.join(
                os.path.dirname(sys.executable),
                'application/configuration.ini'
            )
        else:
            APP_ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
            APP_STATIC = os.path.join(APP_ROOT, 'configuration.ini')

        print('Looking for configuration in {0}'.format(APP_STATIC))
        config = configparser.ConfigParser()
        config.read(APP_STATIC)
        self.db_address = config['ORIG_DB']['db_address']




    def get_example_row_from_db(self):
        """Gets the first row of the database and return it as a dictionary.

        The keys of the dictionary are the column names of the database table,
        the values are the values of the table corresponding to the columns.
        """

        column_names = self.get_table_column_names()
        result = self.conn.execute("SELECT * FROM person").fetchone()
        return {(column_name, result[column_name]) for column_name in column_names}


    def get_table_column_names(self):
        return self.table.columns.keys()

    def get_filtered_resultset(self, where, like):
        try:
            check_where = self.conn.execute("SELECT {} FROM person limit 1".format(where))
            where_column = check_where.fetchone()

            if type(where_column[0]) is int:
                rs = pd.read_sql("SELECT * FROM person WHERE {} = {}".format(where, like), self.engine)
            else:
                rs = pd.read_sql("SELECT * FROM person WHERE {} like '{}'".format(where, like), self.engine)

            return rs
        except exc.SQLAlchemyError as e:
            print("Something went wrong!")
            print(e)

    def get_user_defined_query(self,function, column, where, like):
        try:
            check_column = self.conn.execute("SELECT {} FROM person limit 1".format(column))
            check_where = self.conn.execute("SELECT {} FROM person limit 1".format(where))
            avg_column = check_column.fetchone()
            where_column = check_where.fetchone()

            if function.lower() == 'avg':
                if type(avg_column[0]) is int or type(avg_column[0]) is float:
                    if type(where_column[0]) is int or type(where_column[0]) is float:
                        print("SELECT avg({}) FROM person WHERE {} = {}".format(column, where, like))
                        result = self.conn.execute("SELECT avg({}) FROM person WHERE {} = {}".format(column, where, like))
                        value = result.fetchone()
                    else:
                        result = self.conn.execute("SELECT avg({}) FROM person WHERE {} like '{}'".format(column, where, like))
                        value = result.fetchone()
                else:
                    return "Bad parameter type - column has to be int!"
            elif function.lower() == 'count':
                if type(where_column[0]) is int or type(where_column[0]) is float:
                    result = self.conn.execute("SELECT count({}) FROM person WHERE {} = {}".format(column, where, like))
                    value = result.fetchone()
                else:
                    result = self.conn.execute("SELECT count({}) FROM person WHERE {} like '{}'".format(column, where, like))
                    value = result.fetchone()
            else:
                return "Unknown function - please choose from 'avg' or 'count'!"
            floor = math.floor(value[0])
            return floor
        except exc.SQLAlchemyError as e:
            print("Something went wrong!")
            print(e)


    def get_population_variance_from_db(self,column):
        result = self.conn.execute("SELECT var_pop({}) FROM person".format(column))
        value = result.fetchone()
        return value[0]

    def get_variance_from_filtered_rs(self,column, where, like):
        #DOES NOT WORK YET
        result = self.conn.execute("SELECT var_pop(SELECT {} FROM person where {} = {}) FROM person".format(column, where, like))
        value = result.fetchone()
        return value[0]

    def get_all_data(self):
        return pd.read_sql('SELECT * FROM person WHERE age IS NOT NULL AND income IS NOT NULL', self.engine)

    def get_null_count(self):
        nulls = pd.read_sql('SELECT count(*) FROM person WHERE age IS NULL OR income IS NULL', self.engine, None)
        return "There are " + nulls[0] + " rows with null values. These rows have been ignored."
