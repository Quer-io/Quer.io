from querio.ml.expression.expression import Expression
from enum import Enum


class BoolOp(Enum):
    """An Enum representing the boolean operations and and or."""
    and_ = 'and'
    or_ = 'or'


class ExpressionTreeNode(Expression):
    """Represents an expression tree node.

    This class represents a node in an expression tree of other
    ExpressionTreeNode objects as operands with boolean and and or operators.
    The class supports the python
    operators & and | to create new ExpressionTreeNode objects from existing
    ones or
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
        return ExpressionTreeNode(self, BoolOp.and_, other)

    def __or__(self, other):
        return ExpressionTreeNode(self, BoolOp.or_, other)

    def __iter__(self):
        """Yields all leaf nodes down from this node."""
        for cond in self.leftcond:
            yield cond
        for cond in self.rightcond:
            yield cond

    def eval(self, condition_evaluator):
        """Evaluate this expression.

        Evaluate this expression by evaluating the child expressions and
        combining them with set intersection if op is BoolOp.and_ or
        set union if op is BoolOp.or_.

        Parameters:
        condition_evaluator:
        """
        def or_nodes(left, right, node):
            if node in left and node in right:
                return left[node] | right[node]
            elif node in left:
                return left[node]
            elif node in right:
                return right[node]

        left = self.leftcond.eval(condition_evaluator)
        right = self.rightcond.eval(condition_evaluator)
        if self.op is BoolOp.and_:
            node_set = left.keys() & right.keys()
            return {
                node: left[node] & right[node]
                for node in node_set
            }
        elif self.op is BoolOp.or_:
            node_set = left.keys() | right.keys()
            return {
                node: or_nodes(left, right, node)
                for node in node_set
            }
        else:
            raise NotImplementedError(
                'Unimplemented boolean op {0}'.format(self.op)
            )

    def match(self, feature, value):
        left = self.leftcond.match(feature, value)
        right = self.rightcond.match(feature, value)
        if self.op is BoolOp.and_:
            return left and right
        elif self.op is BoolOp.or_:
            return left or right
        else:
            raise NotImplementedError(
                'Unimplemented boolean op {0}'.format(self.op)
            )
