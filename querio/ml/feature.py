from numbers import Real
from querio.ml.cond import Cond, Op


class Feature:

    def __init__(self, name):
        self.name = name

    def _checktype(self, other, op):
        if(not isinstance(other, Real)):
            raise TypeError(
                '{2} not supported between instances of {0} and {1}'.format(
                    self.__name__, type(other).__name__, op
                )
            )

    def __lt__(self, other):
        self._checktype(other, '<')
        return Cond(self.name, Op.lt, other)

    def __gt__(self, other):
        self._checktype(other, '>')
        return Cond(self.name, Op.gt, other)

    def __le__(self, other):
        self._checktype(other, '<=')
        return self.__lt__(other)

    def __ge__(self, other):
        self._checktype(other, '>=')
        return self.__gt__(other)

    def __eq__(self, other):
        self._checktype(other, '==')
        return Cond(self.name, Op.eq, other)

    # def __ne__(self, other):
    #     self._checktype(other, '!=')
    #     pass
