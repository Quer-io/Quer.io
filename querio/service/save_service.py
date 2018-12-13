import pickle
import re
import os
import shutil
from .exceptions.querio_file_error import QuerioFileError
import logging


class SaveService:
    """Saves and loads created querio models. User can define the path where
        these models are stored.
        Created files have their own naming convention and
        also a unique file name.

        Parameters:
        path: string
            File path where the models are stored
    """

    def __init__(self, path=""):
        """Initialize the SaveService"""
        self._src_folder = path
        self.logger = logging.getLogger("QuerioSaveService")

    def save_model(self, model, name=None):
        """Saves the model into a .querio file.

        :param model: Model
            Created/ modified Model that the users wants to save
        """
        if name is None:
            file_relative_path = self._generate_name_for_model_attributes(
                                            model.output_name,
                                            model.get_feature_names())
        else:
            file_relative_path = name

        dir_relative_path = os.path.join(os.getcwd(), self._src_folder +
                                         file_relative_path[:len(file_relative_path) - 7])

        if not os.path.exists(dir_relative_path):
            os.mkdir(dir_relative_path)

        file = open(os.path.join(dir_relative_path, file_relative_path), 'wb+')
        pickle.dump(model, file)
        file.close()
        self.logger.debug("Saved a model to {}".format(dir_relative_path))

    def load_model(self, output_name, feature_names, model_name=""):
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
        if model_name != "":
            return self.load_file(model_name)
        elif output_name != "" and len(feature_names) > 0:
            return self.load_file(self._generate_name_for_model_attributes(
                output_name,
                feature_names))
        else:
            if output_name == "" or len(feature_names) < 1:
                raise QuerioFileError("Error loading model with output name: '" + output_name + "' " +
                                      "and features: '" + ", ".join(feature_names) + "'")
            elif model_name == "":
                raise QuerioFileError("Error loading model by name: '" + model_name + "'")

    def load_file(self, file_name):
        """Returns Model from the specific file

         :param file_name: string
            Name of the file where Model is stored
        :return:
            Model from the file
        """
        relative_folder_path = self._src_folder + file_name[:len(file_name) - 7]
        relative_file_path = self._src_folder + file_name

        self.logger.debug("Loading a model from '{}'".format(relative_file_path))

        try:
            folder = os.path.join(os.getcwd(), relative_folder_path)
            file = open(os.path.join(folder, relative_file_path), 'rb')
        except FileNotFoundError as e:
            self.logger.error("Could not find a saved model from '{}'"
                              .format(relative_file_path))
            raise QuerioFileError(
                "No model found with following name: " +
                file_name, e)

        try:
            model = pickle.load(file)
        except pickle.PickleError as e:
            self.logger.error("{} could not be loaded as a model"
                              .format(file_name))
            raise QuerioFileError(
                file_name +
                """ could not be loaded as a model.
                Please train a new model""",
                e)
        finally:
            file.close()

        return model

    def clear_querio_files(self):
        """Delete all .querio files from the path folder"""
        path = os.path.join(os.getcwd(), self._src_folder)
        querio_files = self.get_querio_files()

        for file in querio_files:
            querio_file_folder = path + file[:len(file) - 7]
            shutil.rmtree(querio_file_folder)

    def rename_querio_file(self, old_name, new_name):
        """replaces old querio file and folder with new one"""
        path = os.path.join(os.getcwd(), self._src_folder)
        querio_files = self.get_querio_files()

        for file in querio_files:
            if file == old_name:
                old_querio_file_directory = path + file[:len(file) - 7]
                new_querio_file_directory = path + new_name[:len(new_name) - 7]
                os.rename(old_querio_file_directory, new_querio_file_directory)
                old_file_path = os.path.join(new_querio_file_directory, file)
                new_file_path = os.path.join(new_querio_file_directory, new_name)
                os.rename(old_file_path, new_file_path)

    def set_folder(self, folder_path):
        """Sets new folder path

        :param folder_path: string
            New path for the file where Models are saved
        """
        self._src_folder = folder_path

    def model_is_saved(self, model_name):
        """Checks if the model is saved in path folder

         :param model_name: string
            Name of the saved model
        :return:
           True if model exists else return false
        """
        querio_files = self.get_querio_files()

        for querio_file in querio_files:
            if model_name == querio_file:
                return True

        return False

    def _is_querio_file(self, filename):
        filename_pattern = '^(QUERI_){1}(\S)+(.querio){1}$'

        return re.match(filename_pattern, filename)

    def _is_querio_folder(self, folder_name):
        folder_name_pattern = '^(QUERI_){1}(\S)+'

        return re.match(folder_name_pattern, folder_name)

    def generate_querio_name(self, output_name: str, feature_names: list, model_name: str):
        """Public class for generating querio name. Also checks that file is named correctly
        with querio file naming rules

        :param output_name: string
            output name of the querio object
        :param feature_names: set
            set of the querio objects feature names
        :param model_name: string
            name of the model
        :return:
            name of the querio file
        """
        if output_name != "" and len(feature_names) > 0:
            return self._generate_name_for_model_attributes(output_name, feature_names)
        elif model_name != "":
            if len(model_name) > 255:
                raise QuerioFileError("The file name is too long '>255 characters'")
            else:
                invalid_char_list = self._invalid_file_naming_characters(model_name)
                if len(invalid_char_list) > 0:
                    invalid_characters_string = "'" + ", ".join(invalid_char_list) + "'"
                    raise QuerioFileError("The file name contains following illegal characters: " +
                                          str(invalid_characters_string))
            if re.match('^(QUERI_)+(\S)*(.querio){1}$', model_name):
                return model_name
            elif re.match('^(QUERI_)+(\S)*', model_name):
                return model_name + '.querio'
            elif re.match('^(\S)*(.querio){1}$', model_name):
                return 'QUERI_' + model_name
            else:
                return 'QUERI_' + model_name + '.querio'
        else:
            raise QuerioFileError("Could not generate querio name. Have at least output name and feature names or " +
                                  "just model name. Current output name = '" + output_name + "'" +
                                  ". Feature names: '" + " ,".join(feature_names) + "'" +
                                  ". Model name: '" + model_name + "'")

    def _generate_name_for_model_attributes(self, output_name, feature_names):
        feature_names = sorted(feature_names)
        name = 'QUERI_'  # for attribute outputname

        name += output_name + '_IN'  # for attribute featurenames
        while (len(name) < 100 and len(feature_names) > 0):
            name += '_' + feature_names.pop(0)
        if len(feature_names) > 0:
            name += '_..._'
        name += '.querio'
        return name

    def get_querio_files(self):
        """Return all .querio files in path folder

         :return:
            list of querio files
        """
        path = os.path.join(os.getcwd(), self._src_folder)
        path_files = [file for file in os.listdir(path) if os.path.isdir(file)]
        querio_folders = [folder for folder in path_files if self._is_querio_folder(folder)]
        querio_files = []
        for folder in querio_folders:
            folder_files = os.listdir(os.path.join(path, folder))
            found_files = [file for file in folder_files if self._is_querio_file(file)]
            for file in found_files:
                querio_files.append(file)
        return querio_files

    def _invalid_file_naming_characters(self, file_name):
        # regarding to file naming convention: file name should not exceed 255 characters and
        # should not contain following: / \ " ' * ; - ? [ ] ( ) ~ ! $ { } < > # @ & | space tab newline
        result = re.search(r'[\/\\\"\'\*\;\-\?\[\]\(\)\~\!\$\{\}\<\>\#\@\&\|\s]+', file_name)
        if result is None:
            return []
        else:
            invalid_char_list = []
            for char in result.group():
                invalid_char_list.append(char)
            return invalid_char_list
