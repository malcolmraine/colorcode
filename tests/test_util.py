import unittest
from colorcode import _util


class TestUtil(unittest.TestCase):
    def test_clamp_within_bounds(self):
        # value already between lower and upper should be unchanged
        self.assertEqual(_util.clamp(5, 0, 10), 5)
        self.assertEqual(_util.clamp(0, -1, 1), 0)
        self.assertEqual(_util.clamp(3.14, 0.0, 4.0), 3.14)

    def test_clamp_below_lower(self):
        # values below the lower bound should return the lower bound
        self.assertEqual(_util.clamp(-1, 0, 10), 0)
        self.assertEqual(_util.clamp(-5.5, -5.0, 5.0), -5.0)

    def test_clamp_above_upper(self):
        # values above the upper bound should return the upper bound
        self.assertEqual(_util.clamp(20, 0, 10), 10)
        self.assertEqual(_util.clamp(5.5, -1.0, 5.0), 5.0)

    def test_clamp_type_preservation(self):
        # integers should remain ints when possible, floats remain floats
        self.assertIsInstance(_util.clamp(2, 0, 3), int)
        self.assertIsInstance(_util.clamp(2.5, 0.0, 3.0), float)


if __name__ == "__main__":
    unittest.main()
