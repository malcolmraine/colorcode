import unittest
from colorcode import util


class TestUtil(unittest.TestCase):
    def test_clamp_within_bounds(self) -> None:
        # value already between lower and upper should be unchanged
        self.assertEqual(util.clamp(5, 0, 10), 5)
        self.assertEqual(util.clamp(0, -1, 1), 0)
        self.assertEqual(util.clamp(3.14, 0.0, 4.0), 3.14)

    def test_clamp_below_lower(self) -> None:
        # values below the lower bound should return the lower bound
        self.assertEqual(util.clamp(-1, 0, 10), 0)
        self.assertEqual(util.clamp(-5.5, -5.0, 5.0), -5.0)

    def test_clamp_above_upper(self) -> None:
        # values above the upper bound should return the upper bound
        self.assertEqual(util.clamp(20, 0, 10), 10)
        self.assertEqual(util.clamp(5.5, -1.0, 5.0), 5.0)

    def test_clamp_type_preservation(self) -> None:
        # integers should remain ints when possible, floats remain floats
        self.assertIsInstance(util.clamp(2, 0, 3), int)
        self.assertIsInstance(util.clamp(2.5, 0.0, 3.0), float)

    def test_chromacity_calculations(self) -> None:
        """Chromacity helpers return red/green ratios of total color components."""
        # using simple values
        self.assertEqual(util.calc_red_chromacity(1, 1, 1), 1 / 3)
        self.assertEqual(util.calc_green_chromacity(1, 1, 1), 1 / 3)


if __name__ == "__main__":
    unittest.main()
