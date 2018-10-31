from querio.db import data_accessor as da
from querio.ml import model
from querio.service.save_service import SaveService
from querio.service.utils import get_frequency_count


class Interface:
    def __init__(self, dbpath, savepath=""):
        self.accessor = da.DataAccessor(False, dbpath)
        self.models = {}
        self.columns = self.accessor.get_table_column_names()
        self.__ss__ = SaveService(savepath)

    def train(self, xkey, features):
        print('training new model')
        if xkey not in self.columns:
            raise ValueError(xkey + ': No column of this name in database')
        if type(features) is list:
            for f in features:
                if f.feature not in self.columns:
                    raise ValueError(f.feature + ': No column of this name in database')
        feature_list = sorted(list({Cond.feature for Cond in features}))
        feature_names = ""
        for s in feature_list:
            feature_names += s
        self.models[xkey+':'+feature_names] = model.Model(self.accessor.get_all_data(), feature_list, xkey)
        return self.models[xkey+':'+feature_names]

    def query(self, xkey, conditions):
        feature_names = ""
        for c in conditions:
            if c.feature not in feature_names:
                feature_names += c.feature
        if xkey+':'+feature_names not in self.models:
            self.train(xkey, conditions)
        return self.models[xkey+':'+feature_names].predict(conditions)

    def save_models(self):
        for m in self.models:
            self.__ss__.save_model(self.models[m])

    def load_models(self):
        names = self.__ss__.get_querio_files()
        for n in names:
            mod = self.__ss__.load_file(n)
            features = mod.feature_names
            output = mod.output_name
            feature_names = ""
            for s in features:
                feature_names += s
            self.models[output+':'+feature_names] = mod

    def clear_models(self):
        self.models = {}

    def clear_saved_models(self):
        self.__ss__.clear_querio_files()

    def get_saved_models(self):
        return self.__ss__.get_querio_files()

    def get_frequency(self, values):
        data = self.accessor.get_all_data()
        if type(values) != list:
            if values in self.columns:
                values = [values]
            else:
                raise ValueError(str("Database doesn't contain column with the name '{}'").format(values))
        else:
            for val in values:
                if val in self.columns:
                    continue
                else:
                    raise ValueError(str("Database doesn't contain column with the name '{}'").format(val))
        return get_frequency_count(data, values)
