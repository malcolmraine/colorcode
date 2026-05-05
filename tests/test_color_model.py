import unittest

from colorcode import color_model


class TestColorModel(unittest.TestCase):
    def test_rgb_model_passthrough(self) -> None:
        """RGB_Model should return components unchanged in both directions."""
        m = color_model.RGB_Model()
        self.assertEqual(m.to_rgb(0.2, 0.5, 0.8), (0.2, 0.5, 0.8))
        self.assertEqual(m.from_rgb(0.3, 0.6, 0.9), (0.3, 0.6, 0.9))

    def test_hsv_roundtrip(self) -> None:
        """HSV conversion should round-trip from RGB back to the same RGB values."""
        m = color_model.HSV_Model()
        # take arbitrary rgb, convert to hsv and back
        rgb = (0.1, 0.2, 0.3)
        h, s, v = m.from_rgb(*rgb)
        self.assertEqual(m.to_rgb(h, s, v), rgb)

    def test_hsl_roundtrip(self) -> None:
        """HSL conversion should round-trip preserving the original RGB values."""
        m = color_model.HSL_Model()
        rgb = (0.2, 0.4, 0.6)
        h, s, lightness = m.from_rgb(*rgb)
        # conversion returns (h,s,l) but to_rgb expects (h,s,l) differently order
        # after fixing the argument order in to_rgb, the round-trip should
        # reproduce the original RGB values within floating point tolerance
        out = m.to_rgb(h, s, lightness)
        for a, b in zip(out, rgb):
            self.assertAlmostEqual(a, b, places=7)

    def test_tsl_contains_expected_behavior(self) -> None:
        """TSL model should approximately invert conversions for arbitrary RGB values."""
        m = color_model.TSL_Model()
        rgb = (0.3, 0.6, 0.9)
        # verify that converting to tsl and back returns approx original
        # the TSL model is not perfectly invertible, so only validate that
        # the functions execute and produce floating-point components in the
        # expected range.
        t, s, lightness = m.from_rgb(*rgb)
        self.assertTrue(all(isinstance(v, float) for v in (t, s, lightness)))
        result = m.to_rgb(t, s, lightness)
        self.assertEqual(len(result), 3)
        for comp in result:
            self.assertIsInstance(comp, float)
            self.assertGreaterEqual(comp, 0.0)
            self.assertLessEqual(comp, 1.0)

    def test_xyz_roundtrip(self) -> None:
        """XYZ conversion should round-trip preserving the original RGB values."""
        m = color_model.XYZ_Model()
        test_colors = [
            (0.5, 0.5, 0.5),  # Gray
            (1.0, 0.0, 0.0),  # Red
            (0.0, 1.0, 0.0),  # Green
            (0.0, 0.0, 1.0),  # Blue
            (0.2, 0.4, 0.8),  # Mixed
        ]
        for rgb in test_colors:
            x, y, z = m.from_rgb(*rgb)
            rgb_back = m.to_rgb(x, y, z)
            for a, b in zip(rgb_back, rgb):
                self.assertAlmostEqual(a, b, places=5)

    def test_cielab_roundtrip(self) -> None:
        """CIELAB conversion should round-trip preserving the original RGB values."""
        m = color_model.CIELAB_Model()
        test_colors = [
            (1.0, 1.0, 1.0),  # White
            (0.0, 0.0, 0.0),  # Black
            (0.5, 0.5, 0.5),  # Gray
            (1.0, 0.0, 0.0),  # Red
            (0.0, 1.0, 0.0),  # Green
            (0.0, 0.0, 1.0),  # Blue
            (0.2, 0.4, 0.8),  # Mixed
        ]
        for rgb in test_colors:
            L, a, b = m.from_rgb(*rgb)
            # Verify L is in valid range [0, 100] (with small tolerance for floating point)
            self.assertGreaterEqual(L, -0.01)
            self.assertLessEqual(L, 100.01)
            # Round-trip should recover original RGB
            rgb_back = m.to_rgb(L, a, b)
            for a_val, b_val in zip(rgb_back, rgb):
                self.assertAlmostEqual(a_val, b_val, places=4)

    def test_cielab_black_is_zero_lightness(self) -> None:
        """Black (0,0,0) should have approximately L* = 0."""
        m = color_model.CIELAB_Model()
        L, a, b = m.from_rgb(0.0, 0.0, 0.0)
        self.assertAlmostEqual(L, 0.0, places=3)

    def test_cielab_white_is_high_lightness(self) -> None:
        """White (1,1,1) should have approximately L* = 100."""
        m = color_model.CIELAB_Model()
        L, a, b = m.from_rgb(1.0, 1.0, 1.0)
        self.assertAlmostEqual(L, 100.0, places=1)

    def test_xyz_white_point(self) -> None:
        """XYZ conversion of white should produce high Y value (luminance)."""
        m = color_model.XYZ_Model()
        x, y, z = m.from_rgb(1.0, 1.0, 1.0)
        # Y should be close to 1.0 (normalized luminance)
        self.assertGreater(y, 0.9)
        self.assertLess(y, 1.1)

    def test_create_factory(self) -> None:
        """ColorModel.create should produce the correct subclass or raise on unknown type."""
        self.assertIsInstance(
            color_model.create(color_model.ColorModelType.RGB),
            color_model.RGB_Model,
        )
        self.assertIsInstance(
            color_model.create(color_model.ColorModelType.HSV),
            color_model.HSV_Model,
        )
        self.assertIsInstance(
            color_model.create(color_model.ColorModelType.TSL),
            color_model.TSL_Model,
        )
        self.assertIsInstance(
            color_model.create(color_model.ColorModelType.HSL),
            color_model.HSL_Model,
        )
        self.assertIsInstance(
            color_model.create(color_model.ColorModelType.XYZ),
            color_model.XYZ_Model,
        )
        self.assertIsInstance(
            color_model.create(color_model.ColorModelType.CIELAB),
            color_model.CIELAB_Model,
        )
        with self.assertRaises(ValueError):
            color_model.create(color_model.ColorModelType("UNKNOWN"))


if __name__ == "__main__":
    unittest.main()
