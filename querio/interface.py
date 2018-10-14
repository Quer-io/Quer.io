from querio.db import data_accessor as da
from querio.ml import model


class interface:
    def __init__(self, dbPath):
        self.accessor = da.DataAccessor(False, dbPath)
        self.models = {}
        self.columns = self.accessor.get_table_column_names()

    def train(self, xkey, ykey):
        self.models[xkey+''+ykey] = model.Model(self.accessor.get_all_data(), ykey, xkey)
        print('new model: '+xkey+', '+ykey)
        return self.models[xkey+''+ykey]

    def query(self, xkey, ykey, value):
        if xkey+''+ykey not in self.models:
            self.train(xkey, ykey)
        return self.models[xkey+''+ykey].predict(value)
