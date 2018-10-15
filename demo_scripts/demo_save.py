import querio as q

dB = "postgres://otoihucuckhivv:7b93b9777ab13649dc0af7ef499a699a307c7ffd5ca1733389e1dfb1dac5253a@ec2-54-217-250-0.eu-west-1.compute.amazonaws.com:5432/dab0467utv53cp"
i = q.interface(dB)
model = i.train("income", "age")

i.ss.set_folder("qfiles/")

i.ss.save_model(model)


loaded_model = i.ss.load_model("income", ["age"])

i.ss.clear_querio_files()

print("END")