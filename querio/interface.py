from typing import List, Set

from querio.db import data_accessor as da
from querio.ml import model
from querio.service.save_service import SaveService
from querio.ml.expression.cond import Cond
from querio.ml.expression.expression import Expression
from querio.queryobject import QueryObject
from querio.service.utils import get_frequency_count

import logging


class Interface:
    """The base class through which the Querio library can be used effectively.
    It is recomended to use this class for queries, since it handles all
    necessary functions for the user.

    Parameters:
    dbpath: string
        The path to the database in the form
        postgres://username:password@DatabaseAddress:Port/DatabaseName
    savepath: string, optional
        The path that you wish to save the files into.
        If left blank will be the path from which the program was called.
    model_params: dict, optional
        A keyword arguments dict used to pass arguments to trained models.
        See Scikit Learn documentation on decision tree regressors for
        accepted parameters and theirs function.

    """
    def __init__(self, dbpath,  table_name, savepath="", model_params={}):
        """Initialize Interface."""
        self.table_name = table_name
        self.logger = logging.getLogger("QuerioInterface")
        self.accessor = da.DataAccessor(dbpath, table_name)
        self.model_params = model_params
        self.dbpath = dbpath
        self.models = {}
        self.columns = self.accessor.get_table_column_names()
        self.__ss__ = SaveService(savepath)
        self._load_models()

    def train(self, query_target: str, features: list, model_name: str):
        """Trains a new model for given data using the features provided.

        Arguments:
            query_target: string
                The query_target of the model that will be trained.
            features: list of string
                The column names of features that will be trained for the model
            model_name
                Name of the model
         """
        self._validate_columns([query_target])
        self._validate_columns(features)

        self.logger.info("Training a model for '{}' based on '{}'"
                         .format(query_target, ", ".join(features)))

        self.models[model_name] = model.Model(
                                    self.accessor.get_all_data(),
                                    self.table_name,
                                    model_name,
                                    features,
                                    query_target,
                                    self.dbpath,
                                    self.model_params)
        self.__ss__.save_model(self.models[model_name], model_name)
        return self.models[model_name]

    def object_query(self, q_object: QueryObject, model_name=""):
        """Run new query from models using a QueryObject.
        This will run a query from an existing model,
        or if no such model is found will train a new one
        and then query from that.

        :param q_object: QueryObject
            user defined QueryObject.
        :return:
            A Prediction object that contains the predicted mean and variance
            of samples matching the given conditions.
        """
        return self.expression_query(
            q_object.target, q_object.expression, model_name
        )

    def expression_query(
        self, target: str, expression: Expression, model_name=""
    ):
        feature_names = set()
        for c in expression:
            if isinstance(c, Cond):
                feature_names.add(c.feature)

        if model_name is "":
            model_name = self.__ss__.generate_querio_name(
                target, feature_names, ""
            )
        else:
            model_name = self.__ss__.generate_querio_name("", [], model_name)

        self._validate_columns(feature_names)

        if model_name in self.models:
            return self.models[model_name].query(expression)
        else:
            for model in self.models.values():
                if model.output_name == target:
                    if feature_names.issubset(set(model.feature_names)):
                        return model.query(expression)

            self.logger.info(
                "No model for '{}' based on '{}' found. "
                "Training a new one...".format(
                    target, ", ".join(feature_names)
                )
            )
            self.train(target, feature_names, model_name)
            return self.models[model_name].query(expression)

    def query(self, target: str, conditions: List[Cond], model_name=""):
        """

        :param target: string
        :param conditions: list[Cond]
        :return: a prediction object
        """
        if len(conditions) == 1:
            exp = conditions[0]
        else:
            if any(not isinstance(cond, Cond) for cond in conditions):
                raise TypeError("conditions must be a list of Cond")
            exp = conditions[0] & conditions[1]
            for i in range(2, len(conditions)):
                exp = exp & conditions[i]

        return self.expression_query(target, exp, model_name)

    def save_models(self, names=None):
        """Saves the models of this interface as .querio files in the path
        specified by savepath.
        These can later be loaded to another interface with the load_models
        command. Can be given a list of strings to give custom names for
        models."""
        if names is None:
            for m in self.models:
                self.__ss__.save_model(self.models[m])
        elif len(names) != len(self.models):
            logging.warning(
                "List length does not match number of models. Length is {}, "
                "it should be {}".format(len(names), len(self.models))
            )
        else:
            for m, n in zip(self.models, names):
                self.__ss__.save_model(self.models[m], n)

    def get_models(self):
        """Returns the models in this interface."""
        return self.models.values()

    def _load_models(self):
        """Loads models from the savepath to the interface.
        Will only load models that are from a table with the same name as
        current and with the same columns

        Will ignore any files that do not belong to current table.
        If two tables share same table name and same column names will
        load the model."""
        names = self.__ss__.get_querio_files()
        for n in names:
            try:
                mod = self.__ss__.load_file(n)
                features = mod.feature_names
                output = mod.output_name

                self._validate_columns(features)
                self._validate_columns([output])

                feature_names = ""
                for s in features:
                    feature_names += s
                self.models[n] = mod
            except QuerioColumnError:
                self.logger.error("""Encountered an error when loading file
                                   '{}'. This model could not be loaded"""
                                  .format(n))
                continue

    def retrain_models(self):
        for m in self.get_models():
            features = m.get_feature_names()
            output = m.output_name
            name = m.model_name
            self.train(output, features, name)

    def clear_models(self):
        """Clears the models in this interface.
        Will not delete the save files, but will remove any models in this
        interface instance."""
        self.models = {}

    def clear_saved_models(self):
        """Removes all save files from the save path.
        Will not remove files stored in any interface instance, but will
        remove all save files."""
        self.logger.debug("Clearing all the Querio-files...")
        self.__ss__.clear_querio_files()

    def get_saved_models(self):
        """

        :return: A list containing the names of all save files.
        """
        return self.__ss__.get_querio_files()

    def frequency(self, values):
        data = self.accessor.get_all_data(False)
        if type(values) != list:
            values = [values]
        self._validate_columns(values)
        return get_frequency_count(data, values)

    def list_columns(self):
        return self.columns

    def _validate_columns(self, to_check: Set[str]):
        for check in to_check:
            if check not in self.columns:
                self.logger.error("No column called '{}' in database"
                                  .format(check))
                raise QuerioColumnError(
                    "No column called {} in database".format(check))


class QuerioColumnError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, args, kwargs)
