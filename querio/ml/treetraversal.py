from querio.ml.utils import Population
from querio.ml.utils import calculate_mean_and_variance_from_populations
from querio.ml.expression.cond import Op
from querio.ml.noderesult import NodeResultRange
import functools
import sklearn.tree


class NoMatch(Exception):
    """Thrown from Model.query when no rows match the expression."""
    pass


def query_one_tree(
    decision_tree, expression, feature_names, feature_min_maxes
):
    leaf_dict = expression.eval(functools.partial(
        query_for_one_condition, decision_tree, feature_names,
        feature_min_maxes
    ))
    tree = decision_tree.tree_
    leaf_populations = [
        Population(
            tree.n_node_samples[leaf] * leaf_dict[leaf].match_fraction(),
            tree.value[leaf][0][0],
            tree.impurity[leaf]
        )
        for leaf in leaf_dict.keys()
        if leaf_dict[leaf].match_fraction() > 0
    ]

    if all(pop.samples == 0 for pop in leaf_populations):
        raise NoMatch()

    return calculate_mean_and_variance_from_populations(leaf_populations)


def query_for_one_condition(
    decision_tree, feature_names, feature_min_maxes, condition
):
    """Return the set of node indexes that match the condition."""
    tree = decision_tree.tree_
    feature_index = feature_names.index(condition.feature)
    if condition.feature in feature_min_maxes:
        feature_min_max = feature_min_maxes[condition.feature]
    else:
        feature_min_max = {'min': 0, 'max': 0}
    return recurse_tree_node(
        tree, 0, feature_index, condition,
        feature_min_max['min'], feature_min_max['max']
    )


def recurse_tree_node(tree, node_index, feature_index, cond, min, max):
    def is_leaf_node(node_index):
        return tree.children_left[node_index] == sklearn.tree._tree.TREE_LEAF

    def recurse_both_children(isSkipping=False):
        right = recurse_right_child(isSkipping)
        left = recurse_left_child(isSkipping)
        left.update(right)
        return left

    def recurse_right_child(isSkipping=False):
        next_min = min if isSkipping else tree.threshold[node_index]
        return recurse_tree_node(
            tree, tree.children_right[node_index], feature_index, cond,
            next_min, max
        )

    def recurse_left_child(isSkipping=False):
        next_max = max if isSkipping else tree.threshold[node_index]
        return recurse_tree_node(
            tree, tree.children_left[node_index], feature_index, cond,
            min, next_max
        )

    if is_leaf_node(node_index):
        return {
            node_index: NodeResultRange.from_cond_and_range(min, max, cond)
        }

    op = cond.op
    threshold = cond.threshold

    if tree.feature[node_index] == feature_index:
        if op is Op.eq:
            if threshold <= tree.threshold[node_index]:
                return recurse_left_child()
            else:
                return recurse_right_child()
        elif op is Op.lt:
            if threshold <= tree.threshold[node_index]:
                return recurse_left_child()
            else:
                return recurse_both_children()
        elif op is Op.gt:
            if threshold < tree.threshold[node_index]:
                return recurse_both_children()
            else:
                return recurse_right_child()
        else:
            raise NotImplementedError(
                'Unimplemented comparison {0}'.format(op)
            )
    else:
        return recurse_both_children(isSkipping=True)
