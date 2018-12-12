import os
import unittest
from querio import Interface
from querio.ml.expression.feature import Feature
from querio.queryobject import QueryObject

is_travis = 'TRAVIS' in os.environ

class TravisNormalizedDatabaseTest(unittest.TestCase):


    def setUp(self):
        self.db_uri = 'postgres://postgres:@localhost:5432/normaldb'

    def test_make_query_for_querio_view(self):
        if not is_travis:
            return
        
        i = Interface(dB, 'querio_view')

        object1 = QueryObject('height')
        object1.add((Feature('profession_name') == 'programmer'))
        object1.add(Feature('stars') > 20)

        result1 = i.object_query(object1)

        self.assertTrue(result1 is not None)





