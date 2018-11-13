import intervals as i
from querio.ml.expression.cond import Op


class EqIntervalClass:

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

    def __len__(self):
        return 1


class NodeResultRange:
    EqInterval = EqIntervalClass()

    def from_cond_and_range(min, max, cond):
        if cond.op is Op.eq:
            if min <= cond.threshold <= max:
                interval = NodeResultRange.EqInterval
            else:
                interval = i.empty()
        elif cond.op is Op.lt:
            interval = i.open(min, cond.threshold)
        elif cond.op is Op.gt:
            interval = i.open(cond.threshold, max)
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

    def match_lenght(self):
        return len(self.match_interval)

    def match_fraction(self):
        if self.range() == 0:
            return 1
        else:
            return self.match_lenght() / self.range()

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
