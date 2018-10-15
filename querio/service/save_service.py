import pickle
import re
import os


class SaveService():

    def __init__(self):
        self._src_folder = ""



    def save_model(self, model):
        relative_path = self._src_folder + self.generate_name_for_model_attributes( model.output_name, model.feature_names )
        file = open(os.path.join(os.path.expanduser('~'), relative_path), 'wb+')

        pickle.dump( model, file )

        file.close()

    def load_model(self, output_name, feature_names):
        relative_path = self._src_folder + self.generate_name_for_model_attributes(output_name, feature_names)

        file = open(os.path.join(os.path.expanduser('~'), relative_path), 'rb')
        model = pickle.load(file)
        file.close()

        return model


    def clear_querio_files(self):
        path = os.path.join(os.path.expanduser('~'), self._src_folder)
        querio_files = self.get_querio_files()

        for file in querio_files:
            os.remove( path + file )


    def set_folder (self, folder_path):
        self._src_folder = folder_path


    def model_is_saved(self, model_name):

        querio_files = self.get_querio_files()

        for querio_file in querio_files:
            if model_name == querio_file:
                return True

        return False


    def is_querio_file(self, filename):
        filename_pattern = '^(ON-){1}(\S)+(FN-){1}(\S)+$'

        return re.match(filename_pattern, filename)


    def generate_name_for_model_attributes(self, output_name, feature_names):
        name = 'ON-'   # for attribute outputname

        name += output_name + 'FN-' # for attribute featurenames
        name += '_'.join(feature_names)

        return name

    def get_querio_files(self):
        files = os.listdir(os.path.join(os.path.expanduser('~'), self._src_folder))
        querio_files = filter(self.is_querio_file, files)
        return querio_files

