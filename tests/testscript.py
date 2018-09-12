import unittest
import sys
sys.path.append('../')
import application

__name__ = "main"

def f(x):
    return 30000 + (100 * x)



class Mocktest(unittest.TestCase):

    def test(self):
        self.assertEqual(31500, f(15))

    def testResult(self):
        self.assertEqual(application.ml.model.predict_income(1), 10.5)


if __name__ == '__main__':
    unittest.main()
