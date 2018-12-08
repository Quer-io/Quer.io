import unittest
import pandas as pd

from querio.service.save_service import SaveService
from querio.service.exceptions.querio_file_error import QuerioFileError
from querio.ml.model import Model


class SaveServiceTest(unittest.TestCase):

    def setUp(self):
        self.save_service = SaveService()
        self.save_service.clear_querio_files()
        ages = [22, 44, 36, 64, 32, 86, 11, 45]
        incomes = [age * 301 for age in ages]
        heights = [age * 50 for age in ages]
        github_stars = [age * 20 + 10 for age in ages]
        self.data = pd.DataFrame({
            'age': ages, 'income': incomes, 'height': heights,
            'github_stars': github_stars
        })
        generated_name = self.save_service.generate_querio_name('income', ['height', 'age'], "")
        self.test_model = Model(self.data, 'table', generated_name, ['height', 'age'], 'income', 'path')

    def tearDown(self):
        self.save_service.clear_querio_files()

    def test_name_is_generated_correctly(self):
        model_name = ""
        generated_name = self.save_service.generate_querio_name(self.test_model.output_name, self.test_model.get_feature_names(), model_name)
        expected_name = 'QUERI_income_IN_age_height.querio'

        self.assertEqual(expected_name, generated_name)

    def test_saving_model(self):
        model_name = ""
        file_name = self.save_service.generate_querio_name(self.test_model.output_name,
                                                           self.test_model.get_feature_names(), model_name)

        self.assertFalse(self.save_service.model_is_saved(file_name))

        self.save_service.save_model(self.test_model, file_name)

        self.assertTrue(self.save_service.model_is_saved(file_name))

    def test_loading_model(self):
        model_name = ""
        generated_name = self.save_service.generate_querio_name(self.test_model.output_name,
                                                                self.test_model.get_feature_names(), model_name)
        self.save_service.save_model(self.test_model, generated_name)

        loaded_model = self.save_service.load_model(self.test_model.output_name, list(self.test_model.feature_names), model_name)

        self.assertEqual(self.test_model.get_score_for_test(), loaded_model.get_score_for_test())
        self.assertEqual(self.test_model.get_score_for_train(), loaded_model.get_score_for_train())
        self.assertEqual(self.test_model.output_name, loaded_model.output_name)
        self.assertEqual(self.test_model.get_feature_names(), loaded_model.get_feature_names())

    def test_load_file(self):
        model_name = ""
        generated_name = self.save_service.generate_querio_name(self.test_model.output_name,
                                                                self.test_model.get_feature_names(), model_name)
        self.save_service.save_model(self.test_model, generated_name)

        loaded_model = self.save_service.load_file(generated_name)

        self.assertEqual(self.test_model.get_score_for_test(), loaded_model.get_score_for_test())
        self.assertEqual(self.test_model.get_score_for_train(), loaded_model.get_score_for_train())
        self.assertEqual(self.test_model.output_name, loaded_model.output_name)
        self.assertEqual(self.test_model.get_feature_names(), loaded_model.get_feature_names())

    def test_load_file_with_invalid_name(self):
        with self.assertRaises(QuerioFileError):
            self.save_service.load_file("INVALID_FILE")

    def test_is_querio_file_passes_a_correct_string(self):
        test_string = "QUERI_test_IN_test2_test3.querio"
        self.assertTrue(self.save_service._is_querio_file(test_string))

    def test_is_querio_file_fails_an_invalid_string(self):
        test_string = "Failing_IN_String"
        self.assertFalse(self.save_service._is_querio_file(test_string))

    def test_get_querio_files(self):
        model_name = ""
        generated_name = self.save_service.generate_querio_name(self.test_model.output_name,
                                                                self.test_model.get_feature_names(), model_name)
        self.save_service.save_model(self.test_model, generated_name)

        files = self.save_service.get_querio_files()

        self.assertEqual(1, len(files))

    def test_clear_querio_files(self):
        model_name = ""
        generated_name = self.save_service.generate_querio_name(self.test_model.output_name,
                                                                self.test_model.get_feature_names(), model_name)
        self.save_service.save_model(self.test_model, generated_name)
        files = self.save_service.get_querio_files()
        self.assertEqual(1, len(files))

        self.save_service.clear_querio_files()
        files = self.save_service.get_querio_files()
        self.assertEqual(0, len(files))

    def test_load_invalid_file_to_model(self):
        file_name = self.save_service._generate_name_for_model_attributes(self.test_model.output_name, self.test_model.get_feature_names())
        invalid_file = open(file_name, "w+")
        invalid_file.write("INVALID")
        invalid_file.close()

        with self.assertRaises(QuerioFileError):
            self.save_service.load_file(file_name)
