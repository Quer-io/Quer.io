from querio.db import data_accessor as da
from querio.ml import model
from querio.service.save_service import SaveService
from querio.service.util_service import frequency_count
from querio.queryobject import QueryObject
from querio.ml.expression import Expression

class Interface:
    def __init__(self, dbpath, savepath=""):
        self.accessor = da.DataAccessor(False, dbpath)
        self.models = {}
        self.columns = self.accessor.get_table_column_names()
        self.__ss__ = SaveService(savepath)

    def train(self, target: str, features: list):
        print('training new model')
        if target not in self.columns:
            raise ValueError(target + ': No column of this name in database')
        for f in features:
            self._validate_columns(f)
        feature_list = sorted(list({Cond.feature for Cond in features}))
        feature_names = ""
        for s in feature_list:
            feature_names += s
        self.models[target+':'+feature_names] = model.Model(self.accessor.get_all_data(), feature_list, target)
        return self.models[target+':'+feature_names]

    def object_query(self, q_object: QueryObject):
        feature_names = ""
        for c in q_object.expression:
            if c.feature not in feature_names:
                feature_names += c.feature
        if q_object.target+':'+q_object.expression not in self.models:
            self.train(q_object.target, q_object.expression)
        return self.models[q_object.target+':'+feature_names]

    def query(self, target: str, conditions: Expression):
        feature_names = ""
        for c in conditions:
            if c.feature not in feature_names:
                feature_names += c.feature
        if target+':'+feature_names not in self.models:
            self.train(target, conditions)
        return self.models[target+':'+feature_names].predict(conditions)

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

    def frequency(self, values):
        data = self.accessor.get_all_data()
        if type(values) != list:
            if values in self.columns:
                values = [values]
            else:
                raise ValueError(str("Database doesn't contain column with the name '{}'").format(values))
        else:
            for val in values:
                if val not in self.columns:
                    raise ValueError(str("Database doesn't contain column with the name '{}'").format(val))
        return frequency_count(data, values)

    def _validate_columns(self, to_check):
            if to_check not in self.columns:
                raise QuerioColumnError("No column called " + to_check + "in database")


class QuerioColumnError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, args, kwargs)
