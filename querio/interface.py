from querio.db import data_accessor as da
from querio.ml import model, cond
from querio.service.save_service import SaveService


class Interface:
    def __init__(self, dbpath, savepath=""):
        self.accessor = da.DataAccessor(False, dbpath)
        self.models = {}
        self.columns = self.accessor.get_table_column_names()
        self.__ss__ = SaveService(savepath)

    def train(self, xkey, ykey):
        print('training new model')
        if xkey not in self.columns:
            raise ValueError(xkey + ': No column of this name in database')
        if type(ykey) is list:
            for feature_name in ykey:
                if feature_name not in self.columns:
                    raise ValueError(feature_name + ': No column of this name in database')
        if type(ykey) is list:
            ykey = sorted(ykey)
        feature_names = ""
        for s in ykey:
            feature_names += s
        self.models[xkey+':'+feature_names] = model.Model(self.accessor.get_all_data(), ykey, xkey)
        return self.models[xkey+':'+feature_names]

    def query(self, xkey, conditions):
        feature_names = ""
        for c in conditions:
            feature_names += c.feature
        if xkey+':'+feature_names not in self.models:
            self.train(xkey, feature_names)
        return self.models[xkey+':'+feature_names].predict(conditions)

    def saveModels(self):
        for m in self.models:
            self.__ss__.save_model(self.models[m])

    def loadModels(self):
        names = self.__ss__.get_querio_files()
        for n in names:
            mod = self.__ss__.load_file(n)
            features = mod.feature_names
            output = mod.output_name
            feature_names = ""
            for s in features:
                feature_names += s
            self.models[output+':'+feature_names] = mod

    def clearModels(self):
        self.models = {}

    def clearSavedModels(self):
        self.__ss__.clear_querio_files()