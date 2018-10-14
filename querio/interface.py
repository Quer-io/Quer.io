from querio.db import data_accessor as da
from querio.ml import model


class interface:
    def __init__(self, dbPath):
        self.accessor = da.DataAccessor(False, dbPath)
        self.models = {}
        self.columns = self.accessor.get_table_column_names()

    def train(self, xkey, ykey):
        if xkey not in self.columns:
            raise ValueError(xkey + ': No column of this name in database')
        if ykey not in self.columns:
            raise ValueError(ykey + ': No column of this name in database')

        self.models[xkey+''+ykey] = model.Model(self.accessor.get_all_data(), ykey, xkey)
        print('new model: '+xkey+', '+ykey)
        return self.models[xkey+''+ykey]

    def query(self, xkey, ykey, value):
        if xkey+''+ykey not in self.models:
            self.train(xkey, ykey)
        return self.models[xkey+''+ykey].predict(value)
