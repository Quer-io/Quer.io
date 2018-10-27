import unittest
from parameterized import parameterized
from querio.ml.expression.cond import Cond
from querio.ml.expression.cond import Op
from querio.ml.expression.feature import Feature


class TestFeature(unittest.TestCase):

    @parameterized.expand([
        ('age', 30),
        ('height', 168)
    ])
    def test_feature_lt_op(self, feature, threshold):
        feat = Feature(feature)
        cond = feat < threshold
        self.assertEqual(feature, cond.feature)
        self.assertAlmostEqual(threshold, cond.threshold)
        self.assertEqual(Op.lt, cond.op)

    @parameterized.expand([
        ('age', 65),
        ('height', 164)
    ])
    def test_feature_gt_op(self, feature, threshold):
        feat = Feature(feature)
        cond = feat > threshold
        self.assertEqual(feature, cond.feature)
        self.assertAlmostEqual(threshold, cond.threshold)
        self.assertEqual(Op.gt, cond.op)

    @parameterized.expand([
        ('age', 36),
        ('height', 174)
    ])
    def test_feature_eq_op(self, feature, threshold):
        feat = Feature(feature)
        cond = feat == threshold
        self.assertEqual(feature, cond.feature)
        self.assertAlmostEqual(threshold, cond.threshold)
        self.assertEqual(Op.eq, cond.op)
