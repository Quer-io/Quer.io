import querio as q

dB = "path"
i = q.interface(dB)
model = i.train("income", "age")
model2 = i.train("age", "income")

result = model.query(30)
print(str(result))  # > (avg income = 1000; variance income = 4000)

result = model2.query(5000)
print(str(result))  # > (avg age = 30; variance age = 10)
