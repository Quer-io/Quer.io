from service import default_service as ds

def baseUi():
    print("Welcome to Quer.io")
    displayExample()
    displayScikit()
    print("\nInitializing database query tests")
    testDBpremadeQ()
    y = input("\n Enter a database column to search average value from: ")
    testDBuserQ(y)
    x = int(input("\nGive age to search: "))
    displayTest(x)

def displayTest(x):
    x = ds.predict(x)
    print("Expected value is " + repr(x))

def displayExample():
    print("The database contains data in this form:")
    print(ds.get_example_from_db())

def displayScikit():
    sci = ds.accuracy()
    print("\nFeatured data: " + str(sci[0]))
    print("Accuracy of estimating Github stars: " + str(sci[1]))

def testDBpremadeQ():
    print("\n****** Testing average age ******")
    col1 = "age"
    print(ds.get_avg_single_param(col1))
    print("\n****** Testing average heigth ******")
    col2 = "height"
    print(ds.get_avg_single_param(col2))
    print("\n****** Testing for bad parameter 'profession' of type varchar *****")
    col3 = "profession"
    print(ds.get_avg_single_param(col3))

def testDBuserQ(param):
    print("\n Average result for your query parameter " + param + "is: ")
    print(ds.get_avg_single_param(param))
