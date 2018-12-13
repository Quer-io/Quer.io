import unittest
import testing.postgresql
import sqlalchemy


from querio.db.data_accessor import DataAccessor
from querio.db.exceptions.querio_database_error import QuerioDatabaseError


class DataAccessorTest(unittest.TestCase):

    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()
        self.engine = sqlalchemy.create_engine(self.postgresql.url())
        self.conn = self.engine.connect()

        for command in self.commands():
            self.conn.execute(command)

    def tearDown(self):
        self.postgresql.stop()

    def test_create_data_accessor_with_invalid_table_name(self):
        with self.assertRaises(QuerioDatabaseError):
            DataAccessor(self.postgresql.url(), "animal")

    def test_get_example_row_if_table_empty(self):
        da = DataAccessor(self.postgresql.url(), "shop")
        with self.assertRaises(QuerioDatabaseError):
            da.get_example_row_from_db()

    def test_get_example_row_if_table_not_empty(self):
        da = DataAccessor(self.postgresql.url(), "car")
        result = da.get_example_row_from_db()
        self.assertGreater(len(result), 0)

    def test_create_data_accessor_with_invalid_db_address(self):
        with self.assertRaises(QuerioDatabaseError):
            DataAccessor("postgres://evil:man@evilhost:666/scamdb", "car")

    def test_get_population_variance_from_integer_columns(self):
        da = DataAccessor(self.postgresql.url(), "car")
        result = da.get_population_variance_from_db("car_price")
        self.assertIsNotNone(result)

    def test_get_population_variance_from_varchar_columns(self):
        da = DataAccessor(self.postgresql.url(), "car")
        with self.assertRaises(QuerioDatabaseError):
            da.get_population_variance_from_db("car_name")

    def test_pop_var_with_invalid_column_name(self):
        da = DataAccessor(self.postgresql.url(), "car")
        with self.assertRaises(QuerioDatabaseError):
            da.get_population_variance_from_db("not_existing")

    def test_that_data_accessor_is_not_vulnerable_to_sql_injections(self):
        with self.assertRaises(QuerioDatabaseError):
            DataAccessor(self.postgresql.url(), "shop; DROP TABLE car;")

    def test_that_pop_var_is_not_vulnerable_to_sql_injections(self):
        da = DataAccessor(self.postgresql.url(), "car")
        with self.assertRaises(QuerioDatabaseError):
            da.get_population_variance_from_db("car_price; DROP TABLE shop;")

    def test_null_count(self):
        da = DataAccessor(self.postgresql.url(), "car")
        nullmsg = da.get_null_count()
        self.assertEqual("There are 1 rows with null values. These rows have been ignored.", nullmsg)


    def commands(self):
        return ("""
            CREATE TABLE car (
                car_id SERIAL PRIMARY KEY,
                car_name VARCHAR(255) NOT NULL,
                car_price INTEGER
            )
            """,
                """
                CREATE TABLE shop (
                    shop_id SERIAL PRIMARY KEY,
                    shop_name VARCHAR(255) NOT NULL
                )
                """,
                """
                INSERT INTO car
                VALUES (
                    1,
                    'subaru impreza',
                    20000
                )""",
                """
                INSERT INTO car
                VALUES (
                    2,
                    'toyota yaris'
                )
                """)
