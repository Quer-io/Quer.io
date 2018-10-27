from enum import Enum


class BoolOp(Enum):
    and_ = 'and'
    or_ = 'or'


class Expression:

    def __init__(self, leftcond, op, rightcond):
        self.leftcond = leftcond
        self.op = op
        self.rightcond = rightcond

    def __and__(self, other):
        return Expression(self, BoolOp.and_, other)

    def __or__(self, other):
        return Expression(self, BoolOp.or_, other)
