import intervals
from querio.ml.expression.cond import Op


class EqIntervalClass:
    """Used in place of an interval when the condition is an equality."""

    def __and__(self, other):
        if isinstance(other, i.Interval) or isinstance(other, EqIntervalClass):
            return self
        else:
            return NotImplemented

    def __or__(self, other):
        if isinstance(other, i.Interval) or isinstance(other, EqIntervalClass):
            return other
        else:
            return NotImplemented


class NodeResultRange:
    """Represents a decision tree node for a condition.

    Contains the minimum and maximum values of the condition's feature in the
    samples this node contains and the interval that matches the condition.

    Supports '&' and '|' operators with other NodeResultRanges. Both
    nrr1 & nrr2 and nrr1 | nrr2 evaluate to a NodeResultRange if
    nrr1.feature_name == nrr2.feature_name, else they evaluate into a
    NodeResult object.
    """
    EqInterval = EqIntervalClass()

    def from_cond_and_range(min, max, cond):
        if cond.op is Op.eq:
            if min <= cond.threshold <= max:
                interval = NodeResultRange.EqInterval
            else:
                interval = intervals.empty()
        elif cond.op is Op.lt:
            if cond.threshold <= max:
                interval = intervals.open(min, cond.threshold)
            else:
                interval = intervals.open(min, max)
        elif cond.op is Op.gt:
            if cond.threshold >= min:
                interval = intervals.open(cond.threshold, max)
            else:
                interval = intervals.open(min, max)
        else:
            raise NotImplementedError(
                'Unimplemented comparison {0}'.format(op)
            )
        return NodeResultRange(interval, cond.feature, min, max)

    def __init__(self, match_interval, feature_name, min, max):
        self.match_interval = match_interval
        self.feature_name = feature_name
        self.min = min
        self.max = max

    def range(self):
        return self.max - self.min

    def match_length(self):
        """Length of the match_interval."""
        if self.match_interval is NodeResultRange.EqInterval:
            return 1
        else:
            return sum(int.upper - int.lower for int in self.match_interval)

    def match_fraction(self):
        if self.range() == 0:
            return 1
        else:
            return self.match_length() / self.range()

    def __and__(self, other):
        if isinstance(other, NodeResult):
            return NodeResult(self.match_fraction()) & other
        elif isinstance(other, NodeResultRange):
            if self.feature_name == other.feature_name:
                combined_match = self.match_interval & other.match_interval
                return NodeResultRange(
                    combined_match, self.feature_name, self.min, self.max
                )
            else:
                return (
                    NodeResult(self.match_fraction())
                    & NodeResult(other.match_fraction())
                )
        else:
            return NotImplemented

    def __or__(self, other):
        if isinstance(other, NodeResult):
            return NodeResult(self.match_fraction()) | other
        elif isinstance(other, NodeResultRange):
            if self.feature_name == other.feature_name:
                combined_match = self.match_interval | other.match_interval
                return NodeResultRange(combined_match, self.feature_name)
            else:
                return (
                    NodeResult(self.match_fraction())
                    | NodeResult(other.match_fraction())
                )
        else:
            return NotImplemented


class NodeResult:
    """Represents the fraction of samples that match an expression for a node.
    """

    def __init__(self, fraction):
        self.fraction = fraction

    def __and__(self, other):
        return NodeResult(self.fraction * other.match_fraction())

    def __or__(self, other):
        return NodeResult(
            1 - ((1 - self.fraction) * (1 - other.match_fraction()))
        )

    def match_fraction(self):
        return self.fraction
