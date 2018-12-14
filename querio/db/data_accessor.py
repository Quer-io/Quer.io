import sqlalchemy
from sqlalchemy import exc
import pandas as pd
import logging

from .exceptions.querio_database_error import QuerioDatabaseError


class DataAccessor:
    """Class that connects to the defined database

        Parameters:
        address: string
            users defined database address
        table_name: string
            name of the table to be used
    """

    def __init__(self, address, table_name):
        """Initialize the class"""
        self.db_address = address
        self.logger = logging.getLogger("QuerioDataAccessor")
        try:
            self.logger.debug("Connecting to database in '{}'"
                              .format(self.db_address))
            self.engine = sqlalchemy.create_engine(self.db_address)
            self.conn = self.engine.connect()
            self.md = sqlalchemy.MetaData()

            try:
                self.table = sqlalchemy.Table(table_name, self.md,
                                              autoload_with=self.engine)
            except exc.NoSuchTableError as e:
                raise QuerioDatabaseError("Could not find table '{}'"
                                          .format(table_name)) from e

            self.table_name = table_name
            self.connected = True
            self.logger.info("Established a connection to the database")
            self.logger.debug(self.get_null_count())
        except exc.OperationalError as e:
            self.connected = False
            self.logger.critical("Could not connect to the database." +
                                 "Check database settings or that the " +
                                 "database is running")
            raise QuerioDatabaseError("Could not form a connection " +
                                      "to the database") from e

    def get_example_row_from_db(self):
        """Returns the first row of the connected database

        :return:
            A dictionary.
            The keys of the dictionary are column names of the database table,
            the values are the values of the table corresponding to the columns
        """
        self.logger.debug("Fetching an example row from table '{}'"
                          .format(self.table_name))
        column_names = self.get_table_column_names()
        result = self.conn.execute("SELECT * FROM {}"
                                   .format(self.table_name)).fetchone()

        if result is None:
            self.logger.error("Error when fetching example row " +
                              "from the database")
            raise QuerioDatabaseError("Could not fetch an example row " +
                                      "from table '{}'"
                                      .format(self.table_name))
        return {column_name: result[column_name] for column_name in
                column_names}

    def get_table_column_names(self):
        """Returns the names of the table columns

        :return:
            list of strings as table column names
        """
        columns = self.table.columns.keys()
        if self.conn.dialect.name == 'mysql' or self.conn.dialect.name == 'sqlite':
            columns.remove('index')
        return columns

    def get_population_variance_from_db(self, query_column):
        """Returns the variance for all the rows in the specified column

        :param column: string
            user defined column from the table
        :return:
            value of the variance as float
        """

        columns = self.get_table_column_names()

        if query_column not in columns:
            self.logger.error("No column '{}'".format(query_column))
            raise QuerioDatabaseError("No column '{}'".format(query_column))

        try:
            self.logger.debug("Getting variance from column '{}'"
                              .format(query_column))

            result = self.conn.execute("SELECT var_pop({}) FROM {}".format(query_column, self.table_name))
        except exc.ProgrammingError as e:
            self.logger.error("Could not fetch variance for column '{}'"
                              .format(query_column))
            raise QuerioDatabaseError("Invalid column type for '{}'. " +
                                      "Could not get population variance"
                                      .format(query_column)) from e

        value = result.fetchone()
        return value[0]

    def get_all_data(self):
        """Returns all the data from the database table

        :return:
            table data as (pandas) DataFrame
        """
        self.logger.debug("Getting all data from table '{}'"
                          .format(self.table_name))
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
            self.engine, chunksize=1000000
        )

    def get_null_count(self):
        """Returns the count of rows with null values from database table

        :return:
            result defined as string
        """
        column_names = self.get_table_column_names()
        query_start = 'SELECT count(*) AS cnt FROM {} WHERE'
        query_end = []
        for column in column_names:
            if column_names.index(column) is 0:
                query_end.append(' {} IS NULL'.format(column))
            else:
                query_end.append(' OR {} IS NULL'.format(column))
        query_end = ''.join(query_end)
        nulls = pd.read_sql((query_start + query_end)
                            .format(self.table_name), self.engine)
        value = nulls['cnt'].to_string(index=False)
        return ("There are " + value + " rows with null values. " +
                "These rows have been ignored.")
