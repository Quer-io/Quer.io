from typing import List
from querio.db import data_accessor as da
from querio.ml import model
from querio.service.save_service import SaveService
from querio.ml.expression.cond import Cond
from querio.ml.expression.expression import Expression
from querio.queryobject import QueryObject
from querio.service.utils import get_frequency_count


class Interface:
    def __init__(self, dbpath, savepath=""):
        self.accessor = da.DataAccessor(False, dbpath)
        self.models = {}
        self.columns = self.accessor.get_table_column_names()
        self.__ss__ = SaveService(savepath)

    def train(self, target: str, features: list):
        print('training new model')

        self._validate_columns([target])
        self._validate_columns(features)

        feature_names = sorted(features)
        self.models[target+':'.join(feature_names)] = model.Model(self.accessor.get_all_data(), features, target)
        return self.models[target+':'.join(feature_names)]

    def object_query(self, q_object: QueryObject):
        feature_names = []
        for c in q_object.expression:
            if isinstance(c, Cond):
                if c.feature not in feature_names:
                    feature_names.append(c.feature)

        self._validate_columns(feature_names)

        if q_object.target+':'+q_object.expression not in self.models:
            self.train(q_object.target, q_object.expression)
        return self.models[q_object.target+':'+feature_names]

    def query(self, target: str, conditions: List[Cond]):
        feature_names = self.__generate_list(conditions)
        self._validate_columns(feature_names)
        feature_names = sorted(feature_names)
        if target+':'.join(feature_names) not in self.models:
            self.train(target, feature_names)
        exp = conditions[0]
        for x in range(1, len(conditions)):
            exp = exp and conditions[x]

        return self.models[target+':'.join(feature_names)].query(exp)

    def __generate_list(self, conditions):
        feature_names = []
        for c in conditions:
            if c.feature not in feature_names:
                feature_names.append(c.feature)
        return feature_names

    def save_models(self):
        for m in self.models:
            self.__ss__.save_model(self.models[m])

    def load_models(self):
        names = self.__ss__.get_querio_files()
        for n in names:
            try:
                mod = self.__ss__.load_file(n)
                features = mod.model_feature_names
                output = mod.output_name

                self._validate_columns(features)
                self._validate_columns(output)

                feature_names = ""
                for s in features:
                    feature_names += s
                self.models[output+':'+feature_names] = mod
            except QuerioColumnError:
                continue

    def clear_models(self):
        self.models = {}

    def clear_saved_models(self):
        self.__ss__.clear_querio_files()

    def get_saved_models(self):
        return self.__ss__.get_querio_files()

    def frequency(self, values):
        data = self.accessor.get_all_data()
        if type(values) != list:
            values = [values]
        self._validate_columns(values)
        return get_frequency_count(data, values)

    def list_columns(self):
        return self.columns

    def _validate_columns(self, to_check: List[str]):
        for check in to_check:
            if check not in self.columns:
                raise QuerioColumnError("No column called {} in database".format(check))


class QuerioColumnError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, args, kwargs)
