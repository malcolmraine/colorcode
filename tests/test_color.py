import unittest
import colorsys

from colorcode import color
from colorcode.default_colors import DefaultColor
from colorcode import color_parser


class TestColor(unittest.TestCase):
    def test_basics(self):
        """Basic properties (rgb/rgba/base) are stored and updated correctly."""
        c = color.Color(10, 20, 30, 40, base=255)
        self.assertEqual(c.rgb, (10, 20, 30))
        self.assertEqual(c.rgba, (10, 20, 30, 40))
        self.assertEqual(c.base, 255)
        c.base = 100
        self.assertEqual(c.base, 100)

    def test_rgb_setter(self):
        """Setting rgb property updates the underlying color components."""
        c = color.Color()
        c.rgb = (100, 150, 200)
        self.assertEqual(c.rgb, (100, 150, 200))

    def test_rgba_setter(self):
        """Setting rgba property updates all four color components."""
        c = color.Color()
        c.rgba = (50, 60, 70, 80)
        self.assertEqual(c.rgba, (50, 60, 70, 80))

    def test_hsv_property(self):
        """Accessing and assigning hsv should reflect correct conversions to/from RGB."""
        c = color.Color(255, 0, 0)
        h, s, v = c.hsv
        self.assertAlmostEqual(h, 0.0)
        self.assertEqual(s, 1.0)
        self.assertEqual(v, 1.0)
        # setter changes rgb values
        c.hsv = (120, 1, 1)  # green
        self.assertEqual(c.rgb, (0, 255, 0))

    def test_tsl_property(self):
        """TSL getters/setters round-trip without altering RGB values appreciably."""
        c = color.Color(10, 20, 30)
        t, s, l = c.tsl
        # roundtrip check
        c.tsl = (t, s, l)
        for a, b in zip(c.rgb, (10, 20, 30)):
            self.assertAlmostEqual(a, b)

    def test_yiq_property(self):
        """YIQ conversion methods should invert each other for the same input."""
        c = color.Color(100, 150, 200)
        y, i, q = c.yiq
        c.yiq = (y, i, q)
        for a, b in zip(c.rgb, (100, 150, 200)):
            self.assertAlmostEqual(a, b)

    def test_hls_property(self):
        """HLS getters/setters preserve the RGB components through round-trip."""
        c = color.Color(100, 150, 200)
        h, l, s = c.hls
        c.hls = (h, l, s)
        for a, b in zip(c.rgb, (100, 150, 200)):
            self.assertAlmostEqual(a, b)

    def test_create_method(self):
        """Color.create handles ints, strings, sequences, and DefaultColor correctly."""
        self.assertEqual(color.Color.create(0).rgb, color.Color(0, 0, 0).rgb)
        self.assertEqual(
            color.Color.create("rgb(255,0,0)").rgb, color.Color(255, 0, 0).rgb
        )
        self.assertEqual(color.Color.create([10, 20, 30]).rgb, (10, 20, 30))
        self.assertEqual(color.Color.create((40, 50, 60)).rgb, (40, 50, 60))
        self.assertEqual(
            color.Color.create(DefaultColor.BLACK).rgb, color.Color(0, 0, 0).rgb
        )

    def test_chromacity_methods(self):
        """Red/green chromacity methods compute proper ratios from RGB components."""
        c = color.Color(100, 150, 200)
        total = c.red + c.green + c.blue
        self.assertEqual(c.red_chromacity(), c.red / total)
        self.assertEqual(c.green_chromacity(), c.green / total)

    def test_saturation_hue_tint(self):
        """saturation(), hue(), and tint() should return expected scalar values."""
        c = color.Color(255, 0, 0)
        self.assertEqual(c.saturation(), 1.0)
        self.assertEqual(c.hue(), 0.0)
        # tint from tsl should be computed without error
        _ = c.tint()

    def test_lighter_darker(self):
        """lighter/darker modify the color's rgb appropriately and in-place."""
        c = color.Color(100, 100, 100)
        orig = c.rgb
        c.lighter(0.5)
        # lighter reduces saturation so rgb changes
        self.assertNotEqual(c.rgb, orig)
        c.darker(0.5)
        # after darker, rgb should be <= previous rgb values
        self.assertTrue(all(v <= orig[i] for i, v in enumerate(c.rgb)))

    def test_opacity(self):
        """opacity() returns the normalized alpha component."""
        c = color.Color(0, 0, 0, a=128)
        self.assertEqual(c.opacity(), 128 / 255)


if __name__ == "__main__":
    unittest.main()
