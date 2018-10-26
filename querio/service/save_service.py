import pickle
import re
import os

from .exceptions.querio_file_error import QuerioFileError


class SaveService():

    def __init__(self, path=""):
        self._src_folder = path

    def save_model(self, model):
        relative_path = self._src_folder + self._generate_name_for_model_attributes(model.output_name, model.get_feature_names())
        file = open(os.path.join(os.getcwd(), relative_path), 'wb+')

        pickle.dump(model, file)

        file.close()

    def load_model(self, output_name, feature_names):
        return self.load_file(self._generate_name_for_model_attributes(output_name, feature_names))

    def load_file(self, file_name):
        relative_path = self._src_folder + file_name

        try:
            file = open(os.path.join(os.getcwd(), relative_path), 'rb')
        except FileNotFoundError as e:
            raise QuerioFileError("No model found with following name: " + file_name, e)

        try:
            model = pickle.load(file)
        except pickle.PickleError as e:
            raise QuerioFileError(file_name + " could not be loaded as a model. Please train a new model", e)
        finally:
            file.close()


        return model

    def clear_querio_files(self):
        path = os.path.join(os.getcwd(), self._src_folder)
        querio_files = self.get_querio_files()

        for file in querio_files:
            os.remove(path + file)

    def set_folder (self, folder_path):
        self._src_folder = folder_path

    def model_is_saved(self, model_name):
        querio_files = self.get_querio_files()

        for querio_file in querio_files:
            if model_name == querio_file:
                return True

        return False

    def _is_querio_file(self, filename):
        filename_pattern = '^(ON-){1}(\S)+(FN-){1}(\S)+(.querio){1}$'

        return re.match(filename_pattern, filename)

    def _generate_name_for_model_attributes(self, output_name, feature_names):
        name = 'ON-'   # for attribute outputname

        name += output_name + 'FN-' # for attribute featurenames
        name += '_'.join(feature_names)
        name += '.querio'
        return name

    def get_querio_files(self):
        files = os.listdir(os.path.join(os.getcwd(), self._src_folder))
        querio_files = [file for file in files if self._is_querio_file(file)]
        return querio_files

