import unittest
import sys
sys.path.append('../')


def f(x):
    return 30000 + (100 * x)


class Mocktest(unittest.TestCase):

    def test(self):
        self.assertEqual(31500, f(15))


if __name__ == '__main__':
    unittest.main()
