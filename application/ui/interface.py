from service import default_service as ds

def baseUi():
    print("****************************************")
    print("*  Welcome to Quer.io CLI application! *")
    print("****************************************")
    test = input("\nWould you like to run tests? (y/n) ").lower()
    if test == "y":
        testDBpremadeQ()
    exit = "y"
    displayExample()
    displayScikit()    
    while(exit=="y"):
        y = input("\nEnter a database column to search average value from: ")
        testDBuserQ(y)
        exit = input("\nEnd of run! Continue? (y/n) ").lower()


def displayExample():
    print("\nThe database contains data in this form:")
    print(ds.get_example_from_db())

def displayScikit():
    sci = ds.accuracy()
    print("\nFeatured data: " + str(sci[0]))
    print("\nAccuracy of estimating Github stars: " + str(sci[1]))

def testDBpremadeQ():
    print("\n**********************************")
    print("*  Initializing DB test queries  *")
    print("**********************************\n")
    print("++++ Testing queries for AVG(param) ++++\n")
    print("-- Testing param == age --")
    col1 = "age"
    print(ds.get_avg_single_param(col1))
    print("\n-- Testing param == height --")
    col2 = "height"
    print(ds.get_avg_single_param(col2))
    print("\n-- Testing param == profession, illegal type varchar --")
    col3 = "profession"
    print(ds.get_avg_single_param(col3))
    print("\n****************")
    print("* End of tests *")
    print("****************\n")

def testDBuserQ(param):
    print("\nAverage result for your query parameter " + param + " is: ")
    print(ds.get_avg_single_param(param))
