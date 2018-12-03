from typing import List
from querio.db import data_accessor as da
from querio.ml import model
from querio.service.save_service import SaveService
from querio.ml.expression.cond import Cond
from querio.queryobject import QueryObject
from querio.service.utils import get_frequency_count
import logging


class Interface:
    def __init__(self, dbpath,  table_name, savepath=""):
        """The base class through which the Querio library can be used effectively.
        It is recomended to use this class for queries, since it handles all necessary functions
        for the user.

        Parameters:
        dbpath: string
            The path to the database in the form postgres://username:password@DatabaseAddress:Port/DatabaseName
        savepath: string, optional
            The path that you wish to save the files into. If left blank will be the path from which the program was called.

        """
        self.table_name = table_name
        self.accessor = da.DataAccessor(dbpath, table_name)
        self.models = {}
        self.columns = self.accessor.get_table_column_names()
        self.__ss__ = SaveService(savepath)

    def train(self, target: str, features: list):
        """Trains a new model for given data using the features provided.

        Arguments:
            target: string
                The target of the model that will be trained.
            features: list of string
                The column names of features that will be trained for the model
         """
        self._validate_columns([target])
        self._validate_columns(features)

        feature_names = sorted(features)
        self.models[target+':'+''.join(feature_names)] = model.Model(self.accessor.get_all_data(), self.table_name, features, target)

    def object_query(self, q_object: QueryObject):
        """Run new query from models using a QueryObject.
        This will run a query from an existing model,
        or if no such model is found will train a new one
        and then query from that.

        :param q_object: QueryObject
            user defined QueryObject.
        :return:
            A Prediction object that contains the predicted mean and variance of
            samples matching the given conditions.
        """

        feature_names = []
        for c in q_object.expression:
            if isinstance(c, Cond):
                if c.feature not in feature_names:
                    feature_names.append(c.feature)

        feature_names = sorted(feature_names)
        self._validate_columns(feature_names)

        if q_object.target+':'+''.join(feature_names) not in self.models:
            self.train(q_object.target, feature_names)
        return self.models[q_object.target+':'+''.join(feature_names)].query(q_object.expression)

    def query(self, target: str, conditions: List[Cond]):
        """

        :param target: string
        :param conditions: list[Cond]
        :return: a prediction object
        """
        
        feature_names = generate_list(conditions)
        self._validate_columns(feature_names)
        if target+':'.join(feature_names) not in self.models:
            self.train(target, feature_names)
        if len(conditions) == 1:
            exp = conditions[0]
        else:
            exp = conditions[0] & conditions[1]
            for i in range(2, len(conditions)):
                exp = exp & conditions[i]
        return self.models[target+':'+''.join(feature_names)].query(exp)

    def save_models(self, names=None):
        """Saves the models of this interface as .querio files in the path specified by savepath.
        These can later be loaded to another interface with the load_models command.
        Can be given a list of strings to give custom names for models."""
        if names is None:
            for m in self.models:
                self.__ss__.save_model(self.models[m])
        elif len(names) != len(self.models):
            logging.warning("List length does not match number of models. Length is "
                            + str(len(names))+" should be " + str(len(self.models)))
        else:
            for m, n in zip(self.models, names):
                self.__ss__.save_model(self.models[m], n)

    def get_models(self):
        """Returns the models in this interface."""
        return self.models.values()

    def load_models(self):
        """Loads models from the savepath to the interface.
        Will only load models that are from a table with the same name as current and with the same columns
        Will ignore any files that do not belong to current table.
        If two tables share same table name and same column names will load the model."""
        names = self.__ss__.get_querio_files()
        for n in names:
            try:
                mod = self.__ss__.load_file(n)
                features = mod.model_feature_names
                output = mod.output_name
                self._validate_columns(features)
                self._validate_columns([output])

                feature_names = ""
                for s in features:
                    feature_names += s
                self.models[output+':'+feature_names] = mod
            except QuerioColumnError:
                continue

    def clear_models(self):
        """Clears the models in this interface.
        Will not delete the save files, but will remove any models in this interface instance."""
        self.models = {}

    def clear_saved_models(self):
        """Removes all save files from the save path.
        Will not remove files stored in any interface instance, but will remove all save files."""
        self.__ss__.clear_querio_files()

    def get_saved_models(self):
        """

        :return: A list containing the names of all save files.
        """
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


def generate_list(conditions):
    """Generates a sorted list without duplicates from given list
    So a list ['b', 'b', 'a'] becomes ['a', 'b']

    Arguments:
        conditions: a list of string
    Returns:
        a sorted list with only one instance of each string.
        """

    feature_names = []
    for c in conditions:
        if c.feature not in feature_names:
            feature_names.append(c.feature)
    return sorted(feature_names)


class QuerioColumnError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, args, kwargs)
