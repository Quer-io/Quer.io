import quer.io as q

dB = "path"
i = q.interface(dB)
object = QueryObject("income")
object.add((cond("age>20") and cond("age<40")) or cond("height>150"))
result = i.make_query(object)
print(result)  # > (avg income = 3599; variance income = 2450)
