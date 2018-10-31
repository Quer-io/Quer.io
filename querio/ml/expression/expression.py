from enum import Enum


class BoolOp(Enum):
    """An Enum representing the boolean operations and and or."""
    and_ = 'and'
    or_ = 'or'


class Expression:
    """Represents an expression tree node.

    This class represents a node in an expression tree of Cond objects as
    operands with boolean and and or operators. The class supports the python
    operators & and | to create new Expression objects from existing ones or
    Cond objects. The most convenient way to create expression objects is to
    first create Feature objects, create Cond objects from them with
    comparisons and finally create Expression objects from them with & and |
    operators.

    Parameters:
    leftcond: Cond or Expression
        The left side of the operation.
    op: BoolOp
        The operation this node represents.
    rightcond: Cond or Expression
        The right side of the operation.

    Examples:
        expression1 & expression2 -- returns a new Expression with expression1
        and expression2 as operands for the and operator.
        (Feature('age') == 30) & (Feature('income') > 5000)
    """

    def __init__(self, leftcond, op, rightcond):
        self.leftcond = leftcond
        self.op = op
        self.rightcond = rightcond

    def __and__(self, other):
        return Expression(self, BoolOp.and_, other)

    def __or__(self, other):
        return Expression(self, BoolOp.or_, other)
