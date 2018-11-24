import pickle
import re
import os
from .exceptions.querio_file_error import QuerioFileError


class SaveService:
    """Saves and loads created querio models. User can define the path where
        these models are stored.
        Created files have their own naming convention and
        also unique file name.

        Parameters:
        path: string
            File path where the models are stored
    """

    def __init__(self, path=""):
        """Initialize the SaveService"""
        self._src_folder = path

    def save_model(self, model):
        """Saves the model into a querio file.

        :param model: Model
            Created/ modified Model that the users wants to save
        """
        relative_path = (self._src_folder +
                         self._generate_name_for_model_attributes(
                                            model.output_name,
                                            model.get_feature_names()))

        file = open(os.path.join(os.getcwd(), relative_path), 'wb+')

        pickle.dump(model, file)

        file.close()

    def load_model(self, output_name, feature_names):
        """Loads specific Model

         :param output_name: string
            The name of the column used to calculate the mean and the
            variance in queries.
        :param feature_names: list of strings
            The names of the columns in the data that are used
            to narrow down the rows.
        :return:
            Model defined by the parameters
        """
        return self.load_file(self._generate_name_for_model_attributes(
                                                                output_name,
                                                                feature_names))

    def load_file(self, file_name):
        """Returns Model from the specific file

         :param file_name: string
            Name of the file where Model is stored
        :return:
            Model from the file
        """
        relative_path = self._src_folder + file_name

        try:
            file = open(os.path.join(os.getcwd(), relative_path), 'rb')
        except FileNotFoundError as e:
            raise QuerioFileError(
                "No model found with following name: " +
                file_name, e)

        try:
            model = pickle.load(file)
        except pickle.PickleError as e:
            raise QuerioFileError(
                        file_name +
                        """ could not be loaded as a model.
                        Please train a new model""",
                        e)
        finally:
            file.close()

        return model

    def clear_querio_files(self):
        """Delete all querio files from the path folder"""
        path = os.path.join(os.getcwd(), self._src_folder)
        querio_files = self.get_querio_files()

        for file in querio_files:
            os.remove(path + file)

    def set_folder(self, folder_path):
        """Sets new folder path

        :param folder_path: string
            New path for the file where Models are saved
        """
        self._src_folder = folder_path

    def model_is_saved(self, model_name):
        """Checks if the model is saved in path folder

         :param model_name: string
            name of the saved model
        :return:
            true if model exists else return false
        """
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

        name += output_name + 'FN-'  # for attribute featurenames
        name += '_'.join(feature_names)
        name += '.querio'
        return name

    def get_querio_files(self):
        """Return all querio files in path folder

         :return:
            list of querio files
        """
        files = os.listdir(os.path.join(os.getcwd(), self._src_folder))
        querio_files = [file for file in files if self._is_querio_file(file)]
        return querio_files
