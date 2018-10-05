from service.database_and_model_service import DatabaseAndModelService

ds = DatabaseAndModelService("age", "income", (True, ''))

def baseUi():
    print("****************************************")
    print("*  Welcome to Quer.io CLI application! *")
    print("****************************************")
    test = input("\nWould you like to run example queries? (y/n) ").lower()
    if test == "y":
        testDBpremadeQ()
    exit = "y"
    displayExample()
    displayScikit()
    while(exit == "y"):
        function = input("\nChoose what function to use, current options are AVG or COUNT: ")
        column = input("\nChoose a column to execute above function on: ")
        where = input("\nChoose a column for where clause: ")
        like = input("\nChoose a value for like clause linked to above where clause: ")
        userQuery(function, column, where, like)

        if column.lower() == "age" or column.lower() == "income":
            showVariance(column)
            rs = filterResultset(where, like)
            print("Proof that filtering works with filterResultSet")
            filtered = rs.filter(items=['{}'.format(column)])
            print(filtered)

        exit = input("\nEnd of run! Continue? (y/n) ").lower()


def printNZ(string):
    print(str(string).strip('0'))


def showVariance(column):
    print("\nVariance for " + column + " is: {}".format(ds.get_population_variance(column)))


def filteredVariance(column, where, like):
    # DO NOT CALL YET, BROKEN
    print("\nVariance for " + column + " is: {}".format(ds.get_filtered_variance(column, where, like)))


def displayExample():
    print("\nThe database contains data in this form:")
    printNZ(ds.get_example_from_db())


def displayScikit():
    sci = ds.get_accuracy()
    print("\nFeatured data: " + str(sci[0]))
    print("\nAccuracy of estimating Github stars: " + str(sci[1]))


def userQuery(function, column, where, like):
    print("\nYou chose to execute function " + function + " for column " + column + " where " + where + " is like " + like)
    print("\nExecuting query...")
    printNZ(ds.get_user_defined_query(function, column, where, like))


def filterResultset(where, like):
    return ds.get_filtered_resultset(where, like)


def testDBpremadeQ():
    print("\n**********************************")
    print("*  Initializing DB queries        *")
    print("**********************************\n")

    print('\n-- Querying -> function == avg, col == age, where == height, like == 185 --')
    func = "avg"
    col = "age"
    where = "height"
    like = 185
    printNZ(ds.get_user_defined_query(func, col, where, like))

    print('\n-- Querying -> function == avg, col == income, where == age, like == 30 --')
    func = "avg"
    col = "income"
    where = "age"
    like = 30
    printNZ(ds.get_user_defined_query(func, col, where, like))

    print('\n-- Querying -> function == avg, col == age, where == height, like == 185, expecting error--')
    func = "avg"
    col = "profession"
    where = "height"
    like = 185
    printNZ(ds.get_user_defined_query(func, col, where, like))

    print('\n-- Querying -> function == count, col == *, where == height, like == 185 --')
    func = "count"
    col = "*"
    where = "height"
    like = 185
    printNZ(ds.get_user_defined_query(func, col, where, like))

    print('\n-- Querying -> function == count, col == *, where == age, like == 30 --')
    func = "count"
    col = "*"
    where = "age"
    like = 30
    printNZ(ds.get_user_defined_query(func, col, where, like))

    print('\n-- Querying -> function == count, col == test, where == age, like == 30, expecting error --')
    func = "count"
    col = "test"
    where = "age"
    like = 30
    printNZ(ds.get_user_defined_query(func, col, where, like))

    print("\n*****************")
    print("* End of queries *")
    print("******************\n")
