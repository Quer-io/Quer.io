from numbers import Real
from querio.ml.expression.cond import Cond, Op


class Feature:
    """A class allowing the easy creation of Cond objects.

    This class allows creating Cond objects using standard python
    comparison operators <, <=, >, >= and ==. The operators >= and <= have
    the same behaviour as their stricter counterparts.

    Parameters:
        name: string
            The name of the feature created Cond objects will use.

    Example:
    Feature('age') > 30 -- returns a Cond object representing the condition
    age > 30
    """

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
        isStr = isinstance(other, str)
        isReal = isinstance(other, Real)
        isBool = isinstance(other, bool)
        if isStr or isReal or isBool:
            return Cond(self.name, Op.eq, other)
        else:
            return NotImplemented

    # def __ne__(self, other):
    #     self._checktype(other, '!=')
    #     pass
