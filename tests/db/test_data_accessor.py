import unittest

from querio.db.data_accessor import DataAccessor
from querio.db.exceptions.querio_database_error import QuerioDatabaseError

class DataAccessorTest(unittest.TestCase):

    def setUp(self):
        self.db_url = "postgres://queriouser:pass1@0.0.0.0:5432/queriodb"

    def test_get_filtered_resultset_with_invalid_columns(self):
        da = DataAccessor(False, self.db_url)

        with self.assertRaises(QuerioDatabaseError):
            da.get_filtered_resultset("xxx", "120")

    