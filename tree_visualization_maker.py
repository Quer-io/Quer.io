import application.ml as ml
import pandas as pd
import graphviz

data = pd.read_csv('documentation/database/data/1000.csv')
model = ml.Model(data, ['age', 'height'], 'income', 5)
dot_data = model.export_graphviz()
graph = graphviz.Source(dot_data)
graph.render('visualizations/tree')
