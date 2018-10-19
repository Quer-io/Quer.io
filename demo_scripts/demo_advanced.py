import querio as q

dB = "postgres://otoihucuckhivv:7b93b9777ab13649dc0af7ef499a699a307c7ffd5ca1733389e1dfb1dac5253a@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/dab0467utv53cp"

i = q.Interface(dB)
# i.clearSavedModels()
i.loadModels()
result = i.query("income", "age", 30)
print(str(result))  # > (avg income = 1000; variance income = 4000)
result = i.query("age", ["income"], 5000)
print(str(result))  # > (avg age = 30; variance age = 10)

i.saveModels()
