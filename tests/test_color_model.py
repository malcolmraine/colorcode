import math
import unittest

from colorcode import color_model


class TestColorModel(unittest.TestCase):
    def test_rgb_model_passthrough(self):
        """RGB_Model should return components unchanged in both directions."""
        m = color_model.RGB_Model()
        self.assertEqual(m.to_rgb(1, 2, 3), (1, 2, 3))
        self.assertEqual(m.from_rgb(4, 5, 6), (4, 5, 6))

    def test_hsv_roundtrip(self):
        """HSV conversion should round-trip from RGB back to the same RGB values."""
        m = color_model.HSV_Model()
        # take arbitrary rgb, convert to hsv and back
        rgb = (0.1, 0.2, 0.3)
        h, s, v = m.from_rgb(*rgb)
        self.assertEqual(m.to_rgb(h, s, v), rgb)

    def test_hsl_roundtrip(self):
        """HSL conversion should round-trip preserving the original RGB values."""
        m = color_model.HSL_Model()
        rgb = (0.2, 0.4, 0.6)
        h, s, l = m.from_rgb(*rgb)
        # conversion returns (h,s,l) but to_rgb expects (h,s,l) differently order
        self.assertEqual(m.to_rgb(h, s, l), rgb)

    def test_tsl_contains_expected_behavior(self):
        """TSL model should approximately invert conversions for arbitrary RGB values."""
        m = color_model.TSL_Model()
        rgb = (0.3, 0.6, 0.9)
        # verify that converting to tsl and back returns approx original
        t, s, l = m.from_rgb(*rgb)
        result = m.to_rgb(t, s, l)
        for a, b in zip(result, rgb):
            self.assertAlmostEqual(a, b, places=5)

    def test_create_factory(self):
        """ColorModel.create should produce the correct subclass or raise on unknown type."""
        self.assertIsInstance(
            color_model.ColorModel.create(color_model.ColorModelType.RGB),
            color_model.RGB_Model,
        )
        self.assertIsInstance(
            color_model.ColorModel.create(color_model.ColorModelType.HSV),
            color_model.HSV_Model,
        )
        self.assertIsInstance(
            color_model.ColorModel.create(color_model.ColorModelType.TSL),
            color_model.TSL_Model,
        )
        self.assertIsInstance(
            color_model.ColorModel.create(color_model.ColorModelType.HSL),
            color_model.HSL_Model,
        )
        with self.assertRaises(ValueError):
            color_model.ColorModel.create(color_model.ColorModelType("UNKNOWN"))

    def test_chromacity_calculations(self):
        """Chromacity helpers return red/green ratios of total color components."""
        # using simple values
        self.assertEqual(color_model.calc_red_chromacity(1, 1, 1), 1 / 3)
        self.assertEqual(color_model.calc_green_chromacity(1, 1, 1), 1 / 3)


if __name__ == "__main__":
    unittest.main()
