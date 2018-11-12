import sys
import os.path
sys.path = [os.path.dirname(__file__) + '/..'] + sys.path
import querio as q
from querio.ml.expression import Feature
from querio.queryobject import QueryObject

dB = "postgres://otoihucuckhivv:7b93b9777ab13649dc0af7ef499a699a307c7ffd5ca1733389e1dfb1dac5253a@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/dab0467utv53cp"
i = q.Interface(dB, "person")
i.load_models()
object1 = QueryObject("height")
object1.add((Feature('age') > 30) & (Feature('income') > 6000))
object2 = QueryObject("income")
object2.add((Feature('age') < 30) | (Feature('height') > 150))
result1 = i.object_query(object1)
result2 = i.object_query(object2)
print(result1)  # > (avg income = 3000; variance income = 2000)
print(result2)  # > (avg income = 3000; variance income = 2000)
