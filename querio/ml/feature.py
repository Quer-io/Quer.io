from numbers import Real
from querio.ml.cond import Cond, Op


class Feature:

    def __init__(self, name):
        self.name = name

    def __lt__(self, other):
        if(not isinstance(other, Real)):
            return NotImplemented
        return Cond(self.name, Op.lt, other)

    def __gt__(self, other):
        if(not isinstance(other, Real)):
            return NotImplemented
        return Cond(self.name, Op.gt, other)

    def __le__(self, other):
        if(not isinstance(other, Real)):
            return NotImplemented
        return self.__lt__(other)

    def __ge__(self, other):
        if(not isinstance(other, Real)):
            return NotImplemented
        return self.__gt__(other)

    def __eq__(self, other):
        if(not isinstance(other, Real)):
            return NotImplemented
        return Cond(self.name, Op.eq, other)

    # def __ne__(self, other):
    #     self._checktype(other, '!=')
    #     pass
