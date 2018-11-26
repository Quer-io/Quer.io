import math


class Prediction:

    def __init__(self, mean, variance):
        self.result = mean
        self.variance = variance

    def __str__(self):
        return (
            'Result:' + str(round(self.result, 2)) + ', Standard deviation: ' +
            str(round(self.standard_deviation(), 2))
        )

    def __eq__(self, other):
        if type(other) is not Prediction:
            return False

        return self.result == other.result and self.variance == other.variance

    def standard_deviation(self):
        return math.sqrt(self.variance)
