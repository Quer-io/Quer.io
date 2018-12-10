import unittest
import pandas as pd
import querio.service.utils as ut
from querio.service.exceptions.querio_file_error import QuerioFileError
from querio.ml.model import Model


class UtilstTest(unittest.TestCase):

    def setUp(self):
        ages = [22, 44, 36, 64, 32, 86, 11, 44]
        incomes = [age * 301.2 for age in ages]
        heights = [age * 50 for age in ages]
        github_stars = [age * 20 + 10 for age in ages]
        professions = [
            'accountant', 'janitor', 'president', 'janitor',
            'accountant', 'programmer', 'janitor', 'programmer'
        ]
        is_client = [True, True, False, True, False, False, True, True]
        self.data = pd.DataFrame({
            'age': ages, 'income': incomes, 'height': heights,
            'github_stars': github_stars, 'profession': professions,
            'is_client': is_client
        })

    def test_freq_count_for_int(self):
        values_list = self.data['age'].values.tolist()
        self.assertEqual(type(values_list[0]), int)
        dict = ut.get_frequency_count_int(values_list, 'age')
        self.assertDictEqual(dict, {'age frequencies': {11: 1, 22: 1, 32: 1, 36: 1, 44: 2, 64: 1, 86: 1}})

    def test_freq_count_for_float(self):
        values_list = self.data['income'].values.tolist()
        self.assertEqual(type(values_list[0]), float)
        dict = ut.get_frequency_count_int(values_list, 'income')
        self.assertDictEqual(dict, {'income frequencies': {int(11*301.2): 1, int(22*301.2): 1, int(32*301.2): 1,
                                                           int(36*301.2): 1, int(44*301.2): 2, int(64*301.2): 1,
                                                           int(86*301.2): 1}})

    def test_freq_count_for_str(self):
        values_list = self.data['profession'].values.tolist()
        self.assertEqual(type(values_list[0]), str)
        dict = ut.get_frequency_count_str(values_list, 'profession')
        self.assertDictEqual(dict, {'profession frequencies': {'accountant': 2, 'janitor': 3, 'president': 1,
                                                               'programmer': 2}})

    def test_freq_count_for_bool(self):
        values_list = self.data['is_client'].values.tolist()
        self.assertEqual(type(values_list[0]), bool)
        dict = ut.get_frequency_count_bool(values_list, 'is_client')
        self.assertDictEqual(dict, {'is_client frequencies': {True: 5, False: 3}})
