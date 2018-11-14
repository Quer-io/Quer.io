from querio.ml.utils import Population
from querio.ml.utils import calculate_mean_and_variance_from_populations
from querio.ml.expression.cond import Op
import functools
import sklearn.tree


def query_one_tree(decision_tree, expression, feature_names):
    leaf_set = expression.eval(functools.partial(
        query_for_one_condition, decision_tree, feature_names
    ))
    tree = decision_tree.tree_
    leaf_populations = [
        Population(
            tree.n_node_samples[leaf],
            tree.value[leaf][0][0],
            tree.impurity[leaf]
        )
        for leaf in leaf_set
    ]

    return calculate_mean_and_variance_from_populations(leaf_populations)


def query_for_one_condition(decision_tree, feature_names, condition):
    """Return the set of node indexes that match the condition."""
    tree = decision_tree.tree_
    feature_index = feature_names.index(condition.feature)
    return recurse_tree_node(
        tree, 0, feature_index, condition.op, float(condition.threshold)
    )


def recurse_tree_node(tree, node_index, feature_index, op, threshold):
    def is_leaf_node(node_index):
        return tree.children_left[node_index] == sklearn.tree._tree.TREE_LEAF

    def recurse_both_children():
        return recurse_tree_node(
            tree, tree.children_left[node_index], feature_index, op, threshold
        ) | recurse_tree_node(
            tree, tree.children_right[node_index], feature_index, op, threshold
        )

    def recurse_right_child():
        return recurse_tree_node(
            tree, tree.children_right[node_index], feature_index, op, threshold
        )

    def recurse_left_child():
        return recurse_tree_node(
            tree, tree.children_left[node_index], feature_index, op, threshold
        )

    if is_leaf_node(node_index):
        return {node_index}

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
        return recurse_both_children()
