import unittest
from querio import Interface
from querio.ml.expression.feature import Feature
from querio.queryobject import QueryObject
import pandas as pd
from querio.interface import QuerioColumnError
import logging


class MockDataAccessor:
    def __init__(self, db):
        self.db = db

    def get_table_column_names(self):
        return self.db.columns.values

    def get_all_data(self):
        return self.db


def mock_constructor(self, data):
    self.accessor = MockDataAccessor(data)
    self.table_name = 'table'
    self.models = {}
    self.columns = self.accessor.get_table_column_names()
    self.logger = logging.getLogger("QuerioInterface")


class ModelTest(unittest.TestCase):

    def setUp(self):
        ages = [22, 44, 36, 64, 32, 86, 11, 45]
        incomes = [age * 301 for age in ages]
        heights = [age * 50 for age in ages]
        github_stars = [age * 20 + 10 for age in ages]
        professions = [
            'accountant', 'janitor', 'president', 'janitor',
            'accountant', 'programmer', 'janitor', 'programmer'
            ]
        is_client = [True, True, False, True, False, False, False, True]
        data = pd.DataFrame({
            'age': ages, 'income': incomes, 'height': heights,
            'github_stars': github_stars, 'profession': professions,
            'is_client': is_client
        })
        Interface.__init__ = mock_constructor
        self.i = Interface(data)
        self.i.train("github_stars", ["profession", "is_client", "income", "age"])

    def test_query_works_with_valid_number_columns(self):
        try:
            self.i.query("github_stars", [Feature('age') > 30, Feature('income') > 6000])
        except (ValueError, TypeError, QuerioColumnError):
            self.fail()

    def test_query_works_with_valid_string_and_boolean_columns(self):
        try:
            self.i.query("github_stars", [Feature('profession') == 'janitor', Feature('is_client') == True])
        except (ValueError, TypeError, QuerioColumnError):
            self.fail()

    def test_query_works_with_untrained_output(self):
        try:
            self.i.query("age", [Feature('profession') == 'janitor', Feature('is_client') == True])
        except (ValueError, TypeError, QuerioColumnError):
            self.fail()

    def test_query_works_with_untrained_feature_name(self):
        try:
            self.i.query("github_stars", [Feature('height') > 150, Feature('is_client') == False])
        except (ValueError, TypeError, QuerioColumnError):
            self.fail()

    def test_query_errors_with_non_existing_feature_name(self):
        with self.assertRaises(QuerioColumnError):
            self.i.query("github_stars", [Feature('asldjglsagh') == 'janitor', Feature('is_client') == False])

    def test_query_errors_with_non_existing_output_name(self):
        with self.assertRaises(QuerioColumnError):
            self.i.query("adfasdfaf", [Feature('profession') == 'janitor', Feature('is_client') == False])

    def test_query_errors_with_wrong_conditional(self):
        with self.assertRaises(TypeError):
            self.i.query("github_stars", [Feature('profession') > 'janitor', Feature('is_client') > False])

    def test_query_errors_with_invalid_feature(self):
        with self.assertRaises(AttributeError):
            self.i.query("github_stars", "aslfjakfldja")

    def test_query_errors_with_invalid_output_type(self):
        with self.assertRaises(TypeError):
            self.i.query(123, [Feature('profession') == 'janitor', Feature('is_client') == False])

    def test_query_works_with_query_object(self):
        qo = QueryObject("github_stars")
        qo.add((Feature('age') > 30) & (Feature('is_client') == False) & (Feature('profession') == 'janitor'))
        try:
            self.i.object_query(qo)
        except (ValueError, TypeError, QuerioColumnError):
            self.fail()

    def test_query_fails_with_query_object_wrong_output(self):
        qo = QueryObject("age")
        qo.add((Feature('income') > 3000) & (Feature('is_client') == False) & (Feature('profession') == 'janitor'))
        try:
            self.i.object_query(qo)
        except (ValueError, TypeError, QuerioColumnError):
            self.fail()

    def test_query_fails_with_query_object_wrong_conditional(self):
        qo = QueryObject("github_stars")
        qo.add((Feature('age') > 30) & (Feature('is_client') > False) & (Feature('profession') == 'janitor'))
        try:
            self.i.object_query(qo)
        except (ValueError, TypeError, QuerioColumnError):
            self.fail()







