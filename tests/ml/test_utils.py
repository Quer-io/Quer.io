import unittest

from application.ml.utils import make_into_list_if_scalar


class UtilsTest(unittest.TestCase):

    def test_make_into_lest_if_scalar_makes_scalar_into_list(self):
        self.assertListEqual([3], make_into_list_if_scalar(3))

    def test_make_into_lest_if_scalar_keeps_list_unchanged(self):
        list = [1, 2, 3, 4]
        self.assertListEqual(list, make_into_list_if_scalar(list))


if __name__ == '__main__':
    unittest.main()
