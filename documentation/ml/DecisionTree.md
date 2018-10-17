The model class uses a [decision tree regressor](http://scikit-learn.org/stable/modules/tree.html#regression) to
estimate the mean and the variance of the rows of the
data matching the given conditions.

The parameters of the tree are the defaults of scikit
learn, except the random state of the tree is fixed.

The Model class splits the given data to a training
and a test set. The training set is used to train
the decision tree model and the test set is used
to evaluate the performance of the tree. The split
is done with [train_test_split](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) with default parameters,
except the random state is fixed.
