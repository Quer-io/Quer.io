

class Prediction:

    def __init__(self, mean, variance):
        self.result = mean
        self.variance = variance

    def __str__(self):
        return 'Result:' + str(round(self.result, 2)) + ', Variance: ' + str(round(self.variance, 2))


    def __eq__(self, other):
        if type(other) is not Prediction:
            return False

        return self.result == other.result and self.variance == other.variance



