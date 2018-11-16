import sqlalchemy
import psycopg2
from sqlalchemy import exc
import math
import configparser
import os
import pandas as pd
import sys


class DataAccessor:
    """ Class that allows communication with the defined database

        Parameters:
        address: string
            users defined database address
        table_name: string
            name of the table to be used
    """

    def __init__(self, address, table_name):
        """Initialize the class"""
        self.db_address = address
        try:
            self.engine = sqlalchemy.create_engine(self.db_address)
            self.conn = self.engine.connect()
            self.md = sqlalchemy.MetaData()
            self.table = sqlalchemy.Table(table_name, self.md, autoload_with=self.engine)
            self.table_name = table_name
            self.connected = True
            print("Connection established")
            print(self.get_null_count())
        except exc.OperationalError as e:
            print("Invalid database settings. No connection to database")
            self.connected = False
            return

    def get_example_row_from_db(self):
        """ Gets the first row of the database

        :return:
            A dictionary.
            The keys of the dictionary are the column names of the database table,
            the values are the values of the table corresponding to the columns
        """
        column_names = self.get_table_column_names()
        result = self.conn.execute("SELECT * FROM {}".format(self.table_name)).fetchone()
        return {(column_name, result[column_name]) for column_name in column_names}

    def get_table_column_names(self):
        """ Gets the names of the table columns

        :return:
            list of strings as table column names
        """
        return self.table.columns.keys()

    def get_population_variance_from_db(self, column):
        """ Gets the variance for all the rows in the specified column

        :param column: string
            user defined column from the table
        :return:
            value of the variance as float
        """
        result = self.conn.execute("SELECT var_pop({}) FROM {}".format(column, self.table_name))
        value = result.fetchone()
        return value[0]

    def get_all_data(self):
        """ Gets all the data from the database table

        :return:
            table data as (pandas) DataFrame
        """
        column_names = self.get_table_column_names()
        query_start = 'SELECT * FROM {} WHERE'
        query_end = []
        for column in column_names:
            if column_names.index(column) is 0:
                query_end.append(' {} IS NOT NULL'.format(column))
            else:
                query_end.append(' AND {} IS NOT NULL'.format(column))
        query_end = ''.join(query_end)
        return pd.read_sql(
            (query_start + query_end).format(self.table_name),
            self.engine, chunksize=100000
        )

    def get_null_count(self):
        """ Gets the count of rows with null values from database table

        :return:
            result defined as string
        """
        column_names = self.get_table_column_names()
        query_start = 'SELECT count(*) FROM {} WHERE'
        query_end = []
        for column in column_names:
            if column_names.index(column) is 0:
                query_end.append(' {} IS NULL'.format(column))
            else:
                query_end.append(' OR {} IS NULL'.format(column))
        query_end = ''.join(query_end)
        nulls = pd.read_sql((query_start + query_end).format(self.table_name), self.engine)
        value = nulls['count'].to_string(index=False)
        return "There are " + value + " rows with null values. These rows have been ignored."
