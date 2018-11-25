import intervals
import functools
import operator
from querio.ml.expression.cond import Op


class EqIntervalClass:
    """Used in place of an interval when the condition is an equality."""

    def __and__(self, other):
        is_interval = isinstance(other, intervals.Interval)
        is_eq_interval = isinstance(other, EqIntervalClass)
        if is_interval or is_eq_interval:
            return self
        elif isinstance(other, NeqIntervalClass):
            return intervals.empty()
        else:
            return NotImplemented

    def complement(self):
        return NeqInterval

    # def __or__(self, other):
    #     if isinstance(other, i.Interval) or isinstance(other, EqIntervalClass):
    #         return other
    #     else:
    #         return NotImplemented


class NeqIntervalClass:
    def __and__(self, other):
        is_interval = isinstance(other, intervals.Interval)
        is_neq_interval = isinstance(other, NeqIntervalClass)
        if is_interval or is_neq_interval:
            return other
        elif isinstance(other, EqIntervalClass):
            return intervals.empty()
        else:
            return NotImplemented

    def complement(self):
        return EqInterval


EqInterval = EqIntervalClass()
NeqInterval = NeqIntervalClass()


class MinMax:
    def __init__(self, min, max):
        self.min = min
        self.max = max


class NodeResultRange:
    """Represents a decision tree node for a condition.

    Contains the minimum and maximum values of the condition's feature in the
    samples this node contains and the interval that matches the condition.

    Supports & and | operators with other NodeResultRanges.
    nrr1 & nrr2 evaluates to a NodeResultRange if both nrr1.feature_name ==
    nrr2.feature_name.
    """

    def from_cond_and_range(min, max, cond):
        if cond.op is Op.eq:
            if min <= cond.threshold <= max:
                interval = EqInterval
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
        return NodeResultRange(
            {cond.feature: interval}, {cond.feature: MinMax(min, max)}
        )

    def __init__(self, match_intervals, min_maxes):
        self.match_intervals = match_intervals
        self.min_maxes = min_maxes

    def range(self, feature):
        return self.min_maxes[feature].max - self.min_maxes[feature].min

    def match_length(self, feature):
        interval = self.match_intervals[feature]
        if interval is EqInterval:
            return 1
        elif interval is NeqInterval:
            return self.range(feature) - 1
        else:
            return sum(int.upper - int.lower for int in interval)

    def match_fraction(self, feature):
        if self.range(feature) == 0:
            return 1
        else:
            return self.match_length(feature) / self.range(feature)

    def combined_match_fraction(self):
        return functools.reduce(operator.mul, (
            self.match_fraction(feature)
            for feature in self.match_intervals.keys()
        ))

    def __and__(self, other):
        def combine_intervals(ints1, ints2, feature):
            if feature in ints1 and feature in ints2:
                return ints1[feature] & ints2[feature]
            elif feature in ints1:
                return ints1[feature]
            else:
                return ints2[feature]

        if isinstance(other, NodeResultRange):
            intervals = {
                feature: combine_intervals(
                    self.match_intervals, other.match_intervals, feature
                )
                for feature in
                self.match_intervals.keys() | other.match_intervals.keys()
            }
            min_maxes = self.min_maxes
            min_maxes.update(other.min_maxes)
            return NodeResultRange(intervals, min_maxes)
        else:
            return NotImplemented

    def invert(self):
        def invert_interval(feature):
            min_maxes = self.min_maxes[feature]
            return (
                self.match_intervals[feature].complement()
                & intervals.open(min_maxes.min, min_maxes.max)
            )
        match_intervals = {
            feature: invert_interval(feature)
            for feature in self.match_intervals.keys()
        }
        return NodeResultRange(match_intervals, self.min_maxes)

    # def __or__(self, other):
    #     if isinstance(other, NodeResult):
    #         return NodeResult(self.match_fraction()) | other
    #     elif isinstance(other, NodeResultRange):
    #         if self.feature_name == other.feature_name:
    #             combined_match = self.match_interval | other.match_interval
    #             return NodeResultRange(combined_match, self.feature_name)
    #         else:
    #             return (
    #                 NodeResult(self.match_fraction())
    #                 | NodeResult(other.match_fraction())
    #             )
    #     else:
    #         return NotImplemented


# class NodeResult:
#
#     def __init__(self, fraction):
#         self.fraction = fraction
#
#     def __and__(self, other):
#         return NodeResult(self.fraction * other.match_fraction())
#
#     def __or__(self, other):
#         return NodeResult(
#             1 - ((1 - self.fraction) * (1 - other.match_fraction()))
#         )
#
#     def match_fraction(self):
#         return self.fraction
