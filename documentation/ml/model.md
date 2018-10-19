# The Model
The Model class uses a [decision tree regressor](http://scikit-learn.org/stable/modules/tree.html#regression) of scikit learn to
estimate the mean and the variance of the rows of the
data matching the given where-clause. An example
of a decision tree is shown below. The depth of the
tree was limited to 4 to keep the image at a reasonable
size.

![Example decision tree](tree_example.png "Example decision tree")

The parameters of the tree are the defaults of scikit
learn, except the random state of the tree is fixed.

The Model class splits the given data to a training
and a test set. The training set is used to train
the decision tree model and the test set is used
to evaluate the performance of the tree. The split
is done with [train_test_split](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) with default parameters,
except the random state is fixed.

# Queries
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
