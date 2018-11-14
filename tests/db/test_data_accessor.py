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
            da = DataAccessor(self.postgresql.url(), "animal")
    
    def test_get_example_row_if_table_empty(self):
        da = DataAccessor(self.postgresql.url(), "car")
        with self.assertRaises(QuerioDatabaseError):
            result = da.get_example_row_from_db()

    def test_create_data_accessor_with_invalid_db_address(self):
        with self.assertRaises(QuerioDatabaseError):
            da = DataAccessor("postgres://evil:man@evilhost:666/scamdb", "car")

    def test_get_all_data_if_table_empty(self):
        da = DataAccessor(self.postgresql.url(), "car")
        result = da.get_all_data()
        self.assertTrue(result.empty)

    def test_get_population_variance_from_varchar_columns(self):
        da = DataAccessor(self.postgresql.url(), "car")
        with self.assertRaises(QuerioDatabaseError):
            result = da.get_population_variance_from_db("car_name")

    def commands(self):
        return ("""
            CREATE TABLE car (
                car_id SERIAL PRIMARY KEY,
                car_name VARCHAR(255) NOT NULL,
                car_price INTEGER NOT NULL
            )
            """,
            """
            CREATE TABLE shop (
                shop_id SERIAL PRIMARY KEY,
                shop_name VARCHAR(255) NOT NULL
            )
            """)
