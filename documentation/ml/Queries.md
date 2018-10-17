Currently the format of where-clause of the queries is
x1 = v1 and x2 = v2 and ... xn = vn. The query is
made by first finding the set of all leaf nodes in
the decision tree that match the condition of one
variable. So one set of leaf nodes for x1, one for
x2 and so on. Then the intersection of all the
sets of leaf nodes is found, which gives the leaves
that represent all of the rows that match the given
where-clause. The resulting mean and variance is then
calculated from the means and variances of the
matching leaves.

The set of leaves matching the condition of one
variable is found by searching through the tree,
starting from the root. For each searched node,
if the variable the node is checking isn't the same
as the variable the search is for, the search
proceeds to both of the nodes children. If the nodes
variable is the same as the searched variable, the
condition on the node is checked. If the value of
the searched variable matches the condition of the
node, the search proceeds only to the left child
of the node. Otherwise, the search proceeds only to
the right child. The set resulting from the search
is the set of all leaf nodes found by the search.
