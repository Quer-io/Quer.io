import sys
import os.path
sys.path = [os.path.dirname(__file__) + '/..'] + sys.path
import quer.io as q

dB = "postgres://otoihucuckhivv:7b93b9777ab13649dc0af7ef499a699a307c7ffd5ca1733389e1dfb1dac5253a@ec2-54-217-250-0.eu" \
     "-west-1.compute.amazonaws.com:5432/dab0467utv53cp "
i = q.Interface(dB)
object = QueryObject("income")
object.add(cond("age<40") and cond("height>150"))
result = i.make_query(object)
print(result)  # > (avg income = 3000; variance income = 2000)
