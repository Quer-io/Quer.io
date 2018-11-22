# The Model
The Model class uses a [decision tree regressor](http://scikit-learn.org/stable/modules/tree.html#regression) of scikit learn to
estimate the mean and the variance of a column for the
rows of the data matching the given where-clause. The
column the mean and variance are calculated from
is called the output and the columns the where-clause
uses to narrow down the rows are called features.
The output must be continuous. Features can be
continuous, categorical or boolean.

An
example of a decision tree is shown below. The depth of
the tree was limited to 4 to keep the image at a
reasonable size.

![Example decision tree](tree_example.png "Example decision tree")

The parameters of the tree are the defaults of scikit
learn, except the random state of the tree is fixed,
and the depth of the tree can be limited.

The Model class splits the given data to a training
and a test set. The training set is used to train
the decision tree model and the test set is used
to evaluate the performance of the tree. The split
is done with [train_test_split](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) with default parameters,
except the random state is fixed.

When using a large dataset, Model supports the objects
that pandas returns from read_* methods with [chunksize](https://pandas.pydata.org/pandas-docs/stable/io.html#io-chunking)
set. For each chunk the object yields when iterated,
one decision tree is created. Queries are made on all
trees, and their results are averaged for the final
result.

# Queries
The where-clause can contain an arbitrary expression of
conditions combined with "and" and "or" operators.
Each condition is of the form "*feature* > *c*", where
*feature* is one of the features of the model and
*c* is an arbitrary real number. The lesser than and
equality comparisons are also supported. If *feature*
is categorical or a boolean, only equality is supported.

The query is made by traversing the tree for each
condition and combining the results.

## Traversing the tree

The tree is traversed for each condition by starting
from the root and doing the following for each
encountered node. Below *value* is the constant of the
condition and *threshold* is the threshold of a
decision tree node that is being processed.
While traversing, the minimum and the maximum values
that the condition's feature can have in a node
is being kept track of by the variables *min* and
*max*. They are initialized to the minimum and maximum
value of the feature in the entire dataset. When
proceeding to a left, child, *max* is updated to
*threshold* and when proceeding to a right child,
*min* is updated to *threshold*, except as noted
below.
* If the feature of a node not the same as the feature
of the condition, proceed to both of the nodes
children and don't update *min* and *max*.
* If the feature of the node is the same as the
feature of the condition, proceed to one or both of
the children as follows:
  * If the condition is an equality, proceed to the
  left child, if *value* <= *threshold*, otherwise
  proceed to the right child.
  * If the condition is a lesser than, proceed to the
  left child, if *value* <= *threshold*, otherwise
  proceed to both children.
  * If the condition is a greater than, proceed to the
  right child, if *value* >= *threshold*, otherwise
  proceed to both children.
* If the node is a leaf, return a dictionary with one
(*key*, *nrr*) pair, *key* being the index of the
node and *nrr* being a NodeResultRange for the
condition and *min* and *max*.

The dictionaries returned by all encountered leaf nodes
are combined into one result for the condition. As
each leaf is only encountered once, the dictionaries
for all leaves cannot have duplicate keys.

## Combining the results
