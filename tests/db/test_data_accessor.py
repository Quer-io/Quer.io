import unittest

from querio.db.data_accessor import DataAccessor
from querio.db.exceptions.querio_database_error import QuerioDatabaseError

class DataAccessorTest(unittest.TestCase):

    def setUp(self):
        self.db_url = "postgres://queriouser:pass1@0.0.0.0:5432/queriodb"

    def test_create_data_accessor_with_invalid_table_name(self):
       # with self.assertRaises(QuerioDatabaseError):
        da = DataAccessor(False, self.db_url, "INVALID TABLE")
    