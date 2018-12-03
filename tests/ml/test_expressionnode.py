import unittest
from parameterized import parameterized
from querio.ml.expression.feature import Feature


class TestExpressionNode(unittest.TestCase):

    @parameterized.expand([
        ('Simple true', Feature('age') > 30, 'age', 40, True),
        ('Simple false', Feature('age') < 30, 'age', 40, False),
        ('Simple equal', Feature('age') == 30, 'age', 30, True),
        ('Simple not equal', Feature('age') == 30, 'age', 40, False),
        ('Simple limit', Feature('age') < 30, 'age', 30, False),
        ('And true', (
            (Feature('age') > 30) & (Feature('age') < 50)
        ), 'age', 40, True),
        ('And false', (
            (Feature('age') > 30) & (Feature('age') < 50)
        ), 'age', 20, False),
        ('Or true', (
            (Feature('age') > 30) | (Feature('age') < 20)
        ), 'age', 40, True),
        ('Or false', (
            (Feature('age') > 30) | (Feature('age') < 20)
        ), 'age', 25, False),
    ])
    def test_match(self, name, expression, feature, value, is_match):
        match = expression.match(feature, value)
        self.assertEqual(match, is_match)
