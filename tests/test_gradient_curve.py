import math
import unittest

from colorcode import gradient_curve


class TestGradientCurve(unittest.TestCase):
    def test_linear_curve_clamps(self):
        """LinearCurve should clamp inputs outside [0,1] and return x otherwise."""
        curve = gradient_curve.LinearCurve()
        self.assertEqual(curve(-0.5), 0.0)
        self.assertEqual(curve(0.0), 0.0)
        self.assertEqual(curve(0.5), 0.5)
        self.assertEqual(curve(1.0), 1.0)
        self.assertEqual(curve(2.0), 1.0)

    def test_exponential_curve(self):
        """ExponentialCurve should apply exponent then clamp the result."""
        curve = gradient_curve.ExponentialCurve(exponent=2)
        # x**2 clamped
        self.assertEqual(curve(-1.0), 0.0)
        self.assertEqual(curve(0.0), 0.0)
        self.assertEqual(curve(0.5), 0.25)
        self.assertEqual(curve(1.0), 1.0)
        self.assertEqual(curve(2.0), 1.0)

    def test_logarithmic_curve(self):
        """LogarithmicCurve returns zero for x<=0 and factor*log(x)+1 otherwise, clamped."""
        curve = gradient_curve.LogarithmicCurve(factor=0.5)
        # x<=0 returns 0
        self.assertEqual(curve(-1.0), 0.0)
        self.assertEqual(curve(0.0), 0.0)
        # for x>0, factor*log(x)+1 clamped between 0 and 1
        self.assertAlmostEqual(curve(1.0), 1.0)
        # check a value between 0 and 1
        val = curve(0.5)
        expected = 0.5 * math.log(0.5) + 1
        # ensure clamp doesn't change because it's between 0 and 1
        self.assertAlmostEqual(val, expected)


if __name__ == "__main__":
    unittest.main()
