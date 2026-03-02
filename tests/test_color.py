import unittest

from colorcode import color
from colorcode.default_colors import DefaultColor


class TestColor(unittest.TestCase):
    def test_basics(self) -> None:
        """Basic properties (rgb/rgba/base) are stored and updated correctly."""
        c = color.Color(10, 20, 30, 40, base=255)
        self.assertEqual(c.rgb, (10, 20, 30))
        self.assertEqual(c.rgba, (10, 20, 30, 40))
        self.assertEqual(c.base, 255)
        c.base = 100
        self.assertEqual(c.base, 100)

    def test_rgb_setter(self) -> None:
        """Setting rgb property updates the underlying color components."""
        c = color.Color()
        c.rgb = (100, 150, 200)
        self.assertEqual(c.rgb, (100, 150, 200))

    def test_rgba_setter(self) -> None:
        """Setting rgba property updates all four color components."""
        c = color.Color()
        c.rgba = (50, 60, 70, 80)
        self.assertEqual(c.rgba, (50, 60, 70, 80))

    def test_hsv_property(self) -> None:
        """Accessing and assigning hsv should reflect correct conversions to/from RGB."""
        c = color.Color(255, 0, 0)
        h, s, v = c.hsv
        self.assertAlmostEqual(h, 0.0)
        self.assertEqual(s, 1.0)
        self.assertEqual(v, 1.0)
        # setter changes rgb values
        c.hsv = (120, 1, 1)  # green
        self.assertEqual(c.rgb, (0, 255, 0))

    def test_tsl_property(self) -> None:
        """TSL getters/setters can be accessed and assigned without error."""
        c = color.Color(10, 20, 30)
        t, s, lightness = c.tsl
        # setting back should not raise and rgb stays a tuple of numbers
        c.tsl = (t, s, lightness)
        self.assertIsInstance(c.rgb, tuple)
        self.assertEqual(len(c.rgb), 3)

    def test_yiq_property(self) -> None:
        """YIQ getters/setters are callable and yield three-component tuples."""
        c = color.Color(100, 150, 200)
        y, i, q = c.yiq
        c.yiq = (y, i, q)
        self.assertIsInstance(c.rgb, tuple)
        self.assertEqual(len(c.rgb), 3)

    def test_hls_property(self) -> None:
        """HLS getters/setters operate without raising and return three floats."""
        c = color.Color(100, 150, 200)
        h, lightness, s = c.hls
        c.hls = (h, lightness, s)
        self.assertIsInstance(c.rgb, tuple)
        self.assertEqual(len(c.rgb), 3)

    def test_create_method(self) -> None:
        """Color.create handles ints, strings, sequences, and DefaultColor correctly."""
        self.assertEqual(color.Color.create(0).rgb, color.Color(0, 0, 0).rgb)
        self.assertEqual(
            color.Color.create("rgb(255,0,0)").rgb, color.Color(255, 0, 0).rgb
        )
        self.assertEqual(color.Color.create([10, 20, 30]).rgb, (10, 20, 30))
        self.assertEqual(color.Color.create((40, 50, 60)).rgb, (40, 50, 60))
        # DefaultColor enum uses capitalized names
        self.assertEqual(
            color.Color.create(DefaultColor.Black).rgb, color.Color(0, 0, 0).rgb
        )

    def test_chromacity_methods(self) -> None:
        """Red/green chromacity methods compute proper ratios from RGB components."""
        c = color.Color(100, 150, 200)
        total = c.red + c.green + c.blue
        self.assertEqual(c.red_chromacity(), c.red / total)
        self.assertEqual(c.green_chromacity(), c.green / total)

    def test_saturation_hue_tint(self) -> None:
        """saturation(), hue(), and tint() should return expected scalar values."""
        c = color.Color(255, 0, 0)
        self.assertEqual(c.saturation(), 1.0)
        self.assertEqual(c.hue(), 0.0)
        # tint from tsl should be computed without error
        _ = c.tint()

    def test_lighter_darker(self) -> None:
        """lighter/darker modify the color's rgb appropriately and in-place."""
        # use a color with some saturation; pure gray will not change
        c = color.Color(100, 50, 0)
        orig = c.rgb
        c.lighter(0.5)
        # lighter should reduce saturation enough that rgb changes
        self.assertNotEqual(c.rgb, orig)
        c.darker(0.5)
        # after darker, rgb components should not exceed the original
        self.assertTrue(all(v <= orig[i] for i, v in enumerate(c.rgb)))

    def test_opacity(self) -> None:
        """opacity() returns the normalized alpha component."""
        c = color.Color(0, 0, 0, a=128)
        self.assertEqual(c.opacity(), 128 / 255)

    def test_index_packing(self) -> None:
        """__index__ should pack RGBA into a single 32-bit integer correctly."""
        c = color.Color(1, 2, 3, a=4, base=255)
        expected = (1 << 24) | (2 << 16) | (3 << 8) | 4
        self.assertEqual(c.__index__(), expected)


if __name__ == "__main__":
    unittest.main()
