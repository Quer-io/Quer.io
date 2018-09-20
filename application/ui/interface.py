from service import default_service as ds

def baseUi():
    print("Welcome to Quer.io")
    displayExample()
    x = int(input("Give age to search: "))
    displayTest(x)

def displayTest(x):
    x = ds.predict(x)
    print("Expected value is " + repr(x))

def displayExample():
    print("The database contains data in this form:")
    print(ds.get_example_from_db())
