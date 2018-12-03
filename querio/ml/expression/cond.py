from enum import Enum
from querio.ml.expression.expression import Expression
from querio.ml.expression.expressionnode import ExpressionTreeNode, BoolOp


class Op(Enum):
    """An Enum representing lesser than, greater than or equal to in Cond."""
    lt = '<'
    gt = '>'
    eq = '='


class Cond(Expression):
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

    def __and__(self, other):
        return ExpressionTreeNode(self, BoolOp.and_, other)

    def __or__(self, other):
        return ExpressionTreeNode(self, BoolOp.or_, other)

    def __iter__(self):
        yield self

    def eval(self, condition_evaluator):
        return condition_evaluator(self)

    def match(self, feature, value):
        if feature != self.feature:
            return True
        elif self.op is Op.eq:
            return value == self.threshold
        elif self.op is Op.lt:
            return value < self.threshold
        elif self.op is Op.gt:
            return value > self.threshold
        else:
            raise NotImplementedError('{0} is not implemented'.format(self.op))
