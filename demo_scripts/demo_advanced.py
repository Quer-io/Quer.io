import querio as q

dB = "path"
i = q.interface(dB)
result = i.query("income", "age", 30)
print(str(result))  # > (avg income = 1000; variance income = 4000)
result = i.query("age", "income", 5000)
print(str(result))  # > (avg age = 30; variance age = 10)
