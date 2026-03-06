import unittest

from colorcode import gradient, color
from colorcode.gradient import LinearCurve


class TestGradient(unittest.TestCase):
    def test_iteration_linear(self) -> None:
        """Verify that iterating a linear gradient yields evenly spaced RGB results."""
        start = color.Color(0, 0, 0)
        end = color.Color(255, 255, 255)
        grad = gradient.Gradient(start, end, steps=4)
        # four steps should yield 4 colors including end
        results = list(grad)
        # each step increments by 64 (approx)
        expected = [
            color.Color(63.75, 63.75, 63.75),
            color.Color(127.5, 127.5, 127.5),
            color.Color(191.25, 191.25, 191.25),
            color.Color(255, 255, 255),
        ]
        self.assertEqual(len(results), 4)
        for r, e in zip(results, expected):
            self.assertEqual(r.rgb, e.rgb)

    def test_get_color_at_fraction(self) -> None:
        """Ensure get_color returns the correct interpolated color for a given fraction."""
        start = color.Color(0, 0, 0)
        end = color.Color(255, 0, 0)
        grad = gradient.Gradient(start, end, steps=10)
        # 50% along the gradient should be roughly 127.5 red
        mid = grad.get_color(0.5)
        self.assertAlmostEqual(mid.rgb[0], 127.5)
        self.assertEqual(mid.rgb[1], 0)
        self.assertEqual(mid.rgb[2], 0)

    def test_custom_curve(self) -> None:
        """Check that supplying a curve object affects the computed gradient values."""
        start = color.Color(0, 0, 0)
        end = color.Color(0, 255, 0)
        # use a linear curve explicitly
        grad = gradient.Gradient(start, end, curve=LinearCurve(), steps=2)
        # first step at x=0.5
        c = grad.get_color(0.5)
        self.assertAlmostEqual(c.rgb[1], 127.5)


if __name__ == "__main__":
    unittest.main()
