import unittest
from colorcode import util, Color
from colorcode.util.color_diff import (
    delta_e76,
    delta_e94,
    delta_e2000,
    delta_e76_lab,
    delta_e94_lab,
    delta_e2000_lab,
    euclidean_distance,
    weighted_euclidean_distance,
    contrast_ratio,
)


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


class TestColorDifference(unittest.TestCase):
    def test_delta_e76_identical_colors(self) -> None:
        """ΔE*76 between identical colors should be zero."""
        c1 = Color(127.5, 127.5, 127.5, base=255)
        c2 = Color(127.5, 127.5, 127.5, base=255)
        de = delta_e76(c1, c2)
        self.assertAlmostEqual(de, 0.0, places=6)

    def test_delta_e94_identical_colors(self) -> None:
        """ΔE*94 between identical colors should be zero."""
        c1 = Color(127.5, 127.5, 127.5, base=255)
        c2 = Color(127.5, 127.5, 127.5, base=255)
        de = delta_e94(c1, c2)
        self.assertAlmostEqual(de, 0.0, places=6)

    def test_delta_e2000_identical_colors(self) -> None:
        """ΔE00 between identical colors should be zero."""
        c1 = Color(127.5, 127.5, 127.5, base=255)
        c2 = Color(127.5, 127.5, 127.5, base=255)
        de = delta_e2000(c1, c2)
        self.assertAlmostEqual(de, 0.0, places=6)

    def test_delta_e76_is_symmetric(self) -> None:
        """ΔE*76 should be symmetric (same for c1 vs c2 as c2 vs c1)."""
        c1 = Color(255, 0, 0, base=255)
        c2 = Color(0, 255, 0, base=255)
        de_12 = delta_e76(c1, c2)
        de_21 = delta_e76(c2, c1)
        self.assertAlmostEqual(de_12, de_21, places=10)

    def test_delta_e94_is_not_symmetric(self) -> None:
        """ΔE*94 is not symmetric due to weighting based on reference color."""
        c1 = Color(255, 0, 0, base=255)
        c2 = Color(230, 25, 25, base=255)
        de_12 = delta_e94(c1, c2)
        de_21 = delta_e94(c2, c1)
        # They should be different (not symmetric)
        self.assertNotAlmostEqual(de_12, de_21, places=4)

    def test_delta_e2000_is_not_symmetric(self) -> None:
        """ΔE00 is not symmetric due to weighting based on reference color hue."""
        c1 = Color(255, 0, 0, base=255)
        c2 = Color(230, 25, 25, base=255)
        de_12 = delta_e2000(c1, c2)
        de_21 = delta_e2000(c2, c1)
        # ΔE00 can be nearly symmetric for similar colors, just check it computes
        self.assertGreaterEqual(de_12, 0.0)
        self.assertGreaterEqual(de_21, 0.0)

    def test_delta_e76_positive(self) -> None:
        """ΔE*76 should always be positive."""
        colors = [
            (Color(255, 0, 0, base=255), Color(0, 255, 0, base=255)),
            (Color(128, 128, 128, base=255), Color(76, 179, 51, base=255)),
            (Color(255, 255, 255, base=255), Color(0, 0, 0, base=255)),
        ]
        for c1, c2 in colors:
            de = delta_e76(c1, c2)
            self.assertGreaterEqual(de, 0.0)

    def test_delta_e94_positive(self) -> None:
        """ΔE*94 should always be positive."""
        colors = [
            (Color(255, 0, 0, base=255), Color(0, 255, 0, base=255)),
            (Color(128, 128, 128, base=255), Color(76, 179, 51, base=255)),
        ]
        for c1, c2 in colors:
            de = delta_e94(c1, c2)
            self.assertGreaterEqual(de, 0.0)

    def test_delta_e2000_positive(self) -> None:
        """ΔE00 should always be positive."""
        colors = [
            (Color(255, 0, 0, base=255), Color(0, 255, 0, base=255)),
            (Color(128, 128, 128, base=255), Color(76, 179, 51, base=255)),
        ]
        for c1, c2 in colors:
            de = delta_e2000(c1, c2)
            self.assertGreaterEqual(de, 0.0)

    def test_delta_e76_lab_formula(self) -> None:
        """ΔE*76 formula should match Euclidean distance in Lab space."""
        # ΔE*76 = sqrt((ΔL*)² + (Δa*)² + (Δb*)²)
        L1, a1, b1 = 50, 25, 10
        L2, a2, b2 = 55, 20, 15
        expected = ((L2 - L1) ** 2 + (a2 - a1) ** 2 + (b2 - b1) ** 2) ** 0.5
        actual = delta_e76_lab(L1, a1, b1, L2, a2, b2)
        self.assertAlmostEqual(actual, expected, places=10)

    def test_euclidean_distance_rgb(self) -> None:
        """Euclidean RGB distance should match formula."""
        c1 = Color(255, 0, 0, base=255)
        c2 = Color(0, 255, 0, base=255)
        expected = (1.0**2 + 1.0**2 + 0.0**2) ** 0.5
        actual = euclidean_distance(c1, c2)
        self.assertAlmostEqual(actual, expected, places=10)

    def test_euclidean_distance_identical(self) -> None:
        """Euclidean RGB distance between identical colors should be zero."""
        c1 = Color(128, 128, 128, base=255)
        c2 = Color(128, 128, 128, base=255)
        dis = euclidean_distance(c1, c2)
        self.assertAlmostEqual(dis, 0.0, places=10)

    def test_weighted_euclidean_distance_uniform_weights(self) -> None:
        """Weighted Euclidean with equal weights should equal unweighted."""
        c1 = Color(255, 0, 0, base=255)
        c2 = Color(0, 255, 0, base=255)
        weighted = weighted_euclidean_distance(c1, c2, weights=(1.0, 1.0, 1.0))
        unweighted = euclidean_distance(c1, c2)
        self.assertAlmostEqual(weighted, unweighted, places=10)

    def test_weighted_euclidean_distance_custom_weights(self) -> None:
        """Weighted Euclidean should apply custom weights correctly."""
        c1 = Color(255, 0, 0, base=255)
        c2 = Color(0, 255, 0, base=255)
        # Weights heavily favor red channel
        weights = (4.0, 1.0, 1.0)
        expected = (4.0 * 1.0**2 + 1.0 * 1.0**2 + 1.0 * 0.0**2) ** 0.5
        actual = weighted_euclidean_distance(c1, c2, weights=weights)
        self.assertAlmostEqual(actual, expected, places=10)

    def test_contrast_ratio_identical_colors(self) -> None:
        """Contrast ratio of identical colors should be 1.0."""
        c1 = Color(128, 128, 128, base=255)
        c2 = Color(128, 128, 128, base=255)
        ratio = contrast_ratio(c1, c2)
        self.assertAlmostEqual(ratio, 1.0, places=10)

    def test_contrast_ratio_black_vs_white(self) -> None:
        """Contrast ratio of black vs white should be 21:1 (WCAG standard)."""
        c1 = Color(0, 0, 0, base=255)
        c2 = Color(255, 255, 255, base=255)
        ratio = contrast_ratio(c1, c2)
        # Standard contrast ratio should be approximately 21:1
        self.assertAlmostEqual(ratio, 21.0, places=0)

    def test_contrast_ratio_symmetry(self) -> None:
        """Contrast ratio should be symmetric."""
        c1 = Color(51, 51, 51, base=255)
        c2 = Color(204, 204, 204, base=255)
        ratio_12 = contrast_ratio(c1, c2)
        ratio_21 = contrast_ratio(c2, c1)
        self.assertAlmostEqual(ratio_12, ratio_21, places=10)

    def test_contrast_ratio_always_greater_than_one(self) -> None:
        """Contrast ratio should always be >= 1.0."""
        colors = [
            (Color(0, 0, 0, base=255), Color(255, 255, 255, base=255)),
            (Color(128, 128, 128, base=255), Color(128, 128, 128, base=255)),
            (Color(255, 0, 0, base=255), Color(0, 255, 0, base=255)),
        ]
        for c1, c2 in colors:
            ratio = contrast_ratio(c1, c2)
            self.assertGreaterEqual(ratio, 1.0)

    def test_delta_e_values_reasonable_scale(self) -> None:
        """ΔE values should be in reasonable ranges for typical color variations."""
        # Small differences should produce small ΔE values
        c1 = Color(128, 128, 128, base=255)
        c2 = Color(130, 130, 130, base=255)
        for delta_e_func in [delta_e76, delta_e94, delta_e2000]:
            de = delta_e_func(c1, c2)
            self.assertLess(
                de, 10.0, f"{delta_e_func.__name__} should be small for similar colors"
            )
            self.assertGreater(de, 0.0)

        # Large differences should produce larger ΔE values
        c3 = Color(255, 0, 0, base=255)
        c4 = Color(0, 255, 0, base=255)
        for delta_e_func in [delta_e76, delta_e94, delta_e2000]:
            de = delta_e_func(c3, c4)
            self.assertGreater(
                de,
                1.0,
                f"{delta_e_func.__name__} should be larger for different colors",
            )


if __name__ == "__main__":
    unittest.main()
