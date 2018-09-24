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
        function = input("\nChoose what function to use, current options are AVG or COUNT: ")
        column = input("\nChoose a column to execute above function on: ")
        where = input("\nChoose a column for where clause: ")
        like = input("\nChoose a value for like clause linked to above where clause: ")
        userQuery(function, column, where, like)
        if column.lower() == "age" or column.lower() == "income":
            showVariance(column)
        exit = input("\nEnd of run! Continue? (y/n) ").lower()

def printNZ(string):
    print(str(string).strip('0'))

def showVariance(column):
    print("\nVariance for " + column + " is: " + str(ds.get_population_variance(column)))

def displayExample():
    print("\nThe database contains data in this form:")
    printNZ(ds.get_example_from_db())

def displayScikit():
    sci = ds.accuracy()
    print("\nFeatured data: " + str(sci[0]))
    print("\nAccuracy of estimating Github stars: " + str(sci[1]))


def userQuery(function, column, where, like):
    print("\nYou chose to execute function " + function + " for column " + column + " where " + where + " is like " + like)
    print("\nExecuting query...")
    printNZ(ds.get_user_defined_query(function, column, where, like))

def testDBpremadeQ():
    print("\n**********************************")
    print("*  Initializing DB test queries  *")
    print("**********************************\n")

    print("++++ Testing queries for AVG(param) ++++\n")

    print("-- Testing param == age --")
    avg = "age"
    printNZ(ds.get_avg_single_param(avg))

    print("\n-- Testing param == height --")
    avg = "height"
    printNZ(ds.get_avg_single_param(avg))

    print("\n-- Testing param == profession, illegal type varchar --")
    avg = "profession"
    printNZ(ds.get_avg_single_param(avg))

    print("\n++++ Testing queries for AVG(column) with WHERE 'where' and LIKE 'like' ++++")

    print("\n-- Testing column == age, where == height, like == 185 --")
    avg = "age"
    where = "height"
    like = 185
    printNZ(ds.get_avg_three_param(avg, where, like))

    print("\n-- Testing param2 == income, param2 == age, param3 == 30 --")
    avg = "income"
    where = "age"
    like = 30
    printNZ(ds.get_avg_three_param(avg, where, like))

    print("\n-- Testing param1 == profession, param2 == age, param3 == 30, illegal param1 type varchar --")
    avg = "profession"
    printNZ(ds.get_avg_three_param(avg, where, like))

    print("\n++++ Testing user defined query for function 'func', column 'col', where 'where', like 'like'")

    print("\n-- Testing function == avg, col == age, where == height, like == 185 --")
    func = "avg"
    col = "age"
    where = "height"
    like = 185
    printNZ(ds.get_user_defined_query(func, col, where, like))

    print("\n****************")
    print("* End of tests *")
    print("****************\n")
