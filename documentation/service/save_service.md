# Saving models

Interface class uses a class called SaveService to save models to a file. Saved models can later be loaded to use. 
Model-objects are first converted
to binary form using [pickle](http://docs.python.org/3/library/pickle.html).
They are then dumped into a file. 
SaveService will generate a filename based on the output column
the model is trained to predict and the feature columns that the query conditions are 
given to. 

For example if we train a model that would predict **height** based on **income** and
**age** generated filename would be:
 `ON-heightFN-income_age.querio`
 
 ***
 
 Querio uses these filenames to identify models that are saved locally.
 If for some reason there exists a file that is named as shown before but is not a pickled
 model-object an error will be raised to inform that the file could not be unpickled as a 
 model. 
 
 
 ***
 
 Models need to be loaded manually before they can be used. When training a new model, Querio
 checks that has a model with the same output column and feature columns been loaded to the application.
 If yes this model will be loaded instead of training a new one.
 
 If loading is not done and a new model is trained and saved with such columns that
 there already exists a saved model with same columns, **the old file will be overwritten by the
 new one**. This is also needed for example when the database has new data and we need to train 
 a new model
 
 Querio has a functionality to save all the currently trained models 
 and to clear all the saved models in case the user wants to 
 train new models. 
 
 Saving, loading and deleting is all done with **Querio Interface**.
 
 