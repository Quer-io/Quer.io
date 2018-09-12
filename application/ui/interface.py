import ml

def baseUi():
    print("Welcome to Quer.io")
    displayExample()
    x = int(input("Give age to search: "))
    displayTest(x)

def displayTest(x):
    x = ml.predict_income(x)
    print("Expected value is " + repr(x))

def displayExample():
    print("The database contains data in this form:")
    print(ml.get_example_row_from_db())
