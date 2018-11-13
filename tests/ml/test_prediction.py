import unittest

from querio.ml.prediction import Prediction


class PredictTest(unittest.TestCase):

    def test_prediction_prints_correctly(self):
        test_prediction = Prediction(2100.4568, 23.56544)
        prediction_string = str(test_prediction)

        self.assertEqual(
            prediction_string, 'Result:2100.46, Standard deviation: 4.85'
        )

    def test_prediction_equals_true_if_equals(self):
        test_prediction = Prediction(2100.4568, 23.56544)
        test_prediction2 = Prediction(2100.4568, 23.56544)

        self.assertTrue(test_prediction == test_prediction2)

    def test_prediction_equals_false_if_not_equals(self):
        test_prediction = Prediction(2100.4568, 23.56544)
        test_prediction2 = Prediction(21560.4568, 23.56544)

        self.assertFalse(test_prediction == test_prediction2)
