from enum import Enum


class Op(Enum):
    """An Enum representing lesser than, greater than or equal to in Cond."""
    lt = '<'
    gt = '>'
    eq = '='


class Cond:
    """A condition for a feature.
    The condition is of the format
        feature op[<, >, ==] threshold
    The most convenient way to create Cond objects is to use the Feature class.

    Parameters:
    feature: string
        The feature's name.
    op: Op
        The comparison that is made.
    threshold: float
        The value on the right side of the comparison.
    """

    def __init__(self, feature, op, threshold):
        self.feature = feature
        self.op = op
        self.threshold = threshold
