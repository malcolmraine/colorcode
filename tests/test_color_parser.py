import unittest
from colorcode import color_parser


class TestColorParser(unittest.TestCase):
    def test_parse_color_string(self) -> None:
        results = color_parser.parse_color_string("rgb(255,255,255)")
        self.assertListEqual(list(results), [255, 255, 255])

        results = color_parser.parse_color_string("rgb(0,255,255)")
        self.assertListEqual(list(results), [0, 255, 255])

        results = color_parser.parse_color_string("rgb(255,0,255)")
        self.assertListEqual(list(results), [255, 0, 255])

        results = color_parser.parse_color_string("rgba(255,255,255,128)")
        self.assertListEqual(list(results), [255, 255, 255, 128])

        results = color_parser.parse_color_string("rgba(255,255,255,0)")
        self.assertListEqual(list(results), [255, 255, 255, 0])

    def test_parse_hex_string(self) -> None:
        results = color_parser.parse_hex_string("#FFFFFF")
        self.assertListEqual(list(results), [255, 255, 255])

        results = color_parser.parse_hex_string("#1d4ade")
        self.assertListEqual(list(results), [29, 74, 222])

        results = color_parser.parse_hex_string("#c5d948")
        self.assertListEqual(list(results), [197, 217, 72])

        results = color_parser.parse_hex_string("#FFFFFFFF")
        self.assertListEqual(list(results), [255, 255, 255, 255])

        results = color_parser.parse_hex_string("#1d4adeeb")
        self.assertListEqual(list(results), [29, 74, 222, 235])

        results = color_parser.parse_hex_string("#6e1b6bfc")
        self.assertListEqual(list(results), [110, 27, 107, 252])

    def test_parse_color_int(self) -> None:
        results = color_parser.parse_color_int(16777215)
        self.assertListEqual(list(results), [255, 255, 255])

    def test_default_colors_roundtrip(self) -> None:
        """Each DefaultColor should parse and round-trip back to the same hex."""
        from colorcode.default_colors import DefaultColor
        from colorcode import color

        for default in DefaultColor:
            hex_str = str(default)
            # parse the hex and create a Color object
            comps = color_parser.parse_hex_string(hex_str)
            c = color.Color(*comps)
            # convert back to a normalized hex string (ignore case)
            r, g, b = map(int, c.rgb)
            if len(hex_str.strip("#")) == 8:
                # include alpha channel
                a = int(c.rgba[3])
                out_hex = f"#{r:02x}{g:02x}{b:02x}{a:02x}".upper()
            else:
                out_hex = f"#{r:02x}{g:02x}{b:02x}".upper()
            self.assertEqual(out_hex, hex_str.upper(), f"mismatch for {default}")

        results = color_parser.parse_color_int(1919710)
        self.assertListEqual(list(results), [29, 74, 222])

        results = color_parser.parse_color_int(12966216)
        self.assertListEqual(list(results), [197, 217, 72])

        results = color_parser.parse_color_int(4294967295)
        self.assertListEqual(list(results), [255, 255, 255, 255])

        results = color_parser.parse_color_int(491445995)
        self.assertListEqual(list(results), [29, 74, 222, 235])

        results = color_parser.parse_color_int(1847290876)
        self.assertListEqual(list(results), [110, 27, 107, 252])


if __name__ == "__main__":
    unittest.main()
