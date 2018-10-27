from enum import Enum


class Op(Enum):
    lt = '<'
    gt = '>'
    eq = '='


class Cond:

    def __init__(self, feature, op, threshold):
        self.feature = feature
        self.op = op
        self.threshold = threshold
