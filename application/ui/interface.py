import ml

def baseUi():
    print("Welcome to Quer.io")
    x = int(input("Give age to search: "))
    displayTest(x)

def displayTest(x):
    x = ml.predict_income(x)
    print("Expected value is " + repr(x))
