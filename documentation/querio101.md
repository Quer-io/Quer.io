# Usage

In this example we will work with a database table called **person** which has the following information:

| Column | Type |
| --- | --- |
| id | integer |
| age | numeric |
|income       | numeric           |  
 github_stars | numeric           |   
 height       | numeric           |  
 profession   | character varying |
 is_client    | boolean   |
 
 This also corresponds to the sample database this application has been tested with and is provided with the repo as a psql dump file.

 And we have the table in a Postgresql-database which is running with the following settings:

| Setting | Value |
| --- | --- |
| host | localhost |
| port | 5432 |
| username | queriouser |
| password | pass1 |
| database name | queriodb |

 ## Connecting to a database
 
First thing we do is create an **interface** in which we give the database URI and the table name we wish to query. So first we import Querio and create an instance of the interface like this:

```python
import querio

# Here we form a database address based on the settings shown before
db_address = 'postgres://queriouser:pass1@localhost:5432/queriodb'

# We create an instance of interface named 'i' and pass the database address and desired table name to it
i = querio.Interface(db_address, 'person')

```

Now we have an interface! Next we'll see how to make queries.

## Tables and views

Due to the nature of the packages utilized by Querio, it is currently not possible to initialize machine learning processes to multiple tables at the same time. In practice this means that the data should be stored in a single table, though this is not practical in most production databases. This can be circumvented by creating database views that store the the desired data in a single searchable object. Types of views differ between different database systems, but in general if the database is in a stable form and Querio is used on a predetermined set of columns, a materialized view might be a suitable solution. For quick usage normal static views and even temporary views that are deleted after each session.

Creating views with (postgreSQL) is simple, a desired query written and stored as a database view, which can then be queried just like a standard table would be queried. For example:

```sql
CREATE OR REPLACE TEMP VIEW querio_view AS (
   SELECT x.a
          y.b
          z.c
   FROM   x
    INNER JOIN y USING (key)
    INNER JOIN z USING (key)
  );
```

## Making queries

Queries are made by passing a **QueryObject**
 to the interface. When creating a QueryObject we have to define which column we want to estimate.
 
 ```python
from querio.queryobject import QueryObject

# We'll create a QueryObject that estimates the value of height given certain conditions
query_object1 = QueryObject("height")
```

Conditions are given by *adding* them to the QueryObject. A condition is given by creating a **Feature** for a column 
 ```python
from querio.ml.expression import Feature

# We'll add a condition for our query by creating a Feature for column 'age' and a condition that is has to be over 30
query_object1.add((Feature('age') > 30))

# You can also use AND and OR operators when adding conditions like this

#AND
query_object1.add((Feature('github stars') > 45) & (Feature('income') > 6000))

#OR
query_object1.add((Feature('github stars') > 45) | (Feature('income') > 6000))

```

Now all that's left is making the query itself.

 ```python

result = i.object_query(query_object1)

```

Quer.io will now build a model based on the column we wish to query and the columns that are defined in the query conditions if it has not been built before. 

For example now we're making our first query so no models has been built at this point. Quer.io will now build a model for column `height` based on columns `github_stars`, `age` and `income`.

If the database is large this might take while but is only necessary to be done once. Of course if the data in the database changes it will be necessary to do this again for the estimation to be accurate.

`result` is a **Prediction** object which has the prediction itself and the standard deviation of the answer.

If we want to, for example change the values of comparators in the Features like changing the age to be over 45 etc. we don't have to train a new model. We can just create another QueryObject and pass the new parameters to it and Quer.io reuses the same model it built for the first query if all the columns used are same ones that were used in the first query. 

Models can also be saved persistently so that they can be reused even if the program is restarted.


## Saving and loading models

Saving a model is simple. After making a query to the interface we'll just need to call one function in the interface.

 ```python
i.save_models()
```

By default Quer.io saves the models to the same directory that the program is executed from. This can be overridden by passing a *save path* when creating the interface like this

```python
i = querio.Interface(db_address, 'person', savepath='/path/to/your/desired/folder')
```

Quer.io uses this folder also when loading models.

Loading models can also be done easily. Before doing any queries just call the following function

 ```python
i.load_models()
```

Now Quer.io will load every model that it has saved in to the memory and if it detect's that a model has already been trained for the same columns thar are being queried that model will be used instead of training a new one. Quer.io detects every file that ends with .querio so don't remove them if you want to reuse the model later.
