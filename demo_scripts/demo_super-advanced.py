import quer.io as q

dB = "path"
i = q.interface(dB)
object = QueryObject("income")
object.add(cond("age<40") and cond("height>150"))
result = i.make_query(object)
print(result)  # > (avg income = 3000; variance income = 2000)
