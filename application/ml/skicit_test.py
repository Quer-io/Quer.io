import pandas as pd
import numpy as np
import sqlalchemy

from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

db_string = "postgres://otoihucuckhivv:7b93b9777ab13649dc0af7ef499a699a307c7ffd5ca1733389e1dfb1dac5253a@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/dab0467utv53cp"
engine = sqlalchemy.create_engine(db_string)

data = pd.read_sql('SELECT * FROM person', engine)

train, test = train_test_split(data, test_size = 0.15)
c = DecisionTreeClassifier(min_samples_split=10)

#to-do: add profession
features = ["age", "income", "height"]

X_train = train[features]
y_train = train["github_stars"]

X_test = train[features]
y_test = train["github_stars"]

dt = c.fit(X_train, y_train)

y_pred = c.predict(X_test)
score = accuracy_score(y_test, y_pred) * 100

print("Accuracy of estimating Github stars: ", round(score, 1), "%")