"""Example 1 — Parsing & Color.create

Demonstrates parsing hex/rgb/rgba strings, packed integers, and using
`Color.create` to build `Color` instances from different inputs.

Expected output
---------------
parse_hex_string: (29, 74, 222)
parse_color_string (rgb): (255, 0, 128)
parse_color_string (rgba): (255, 0, 128, 64)
parse_color_int (RGB): (29, 74, 222)
parse_color_int (RGBA): (29, 74, 222, 235)
Color.create from int -> rgb: (255.0, 255.0, 255.0)
Color.create from string -> rgb: (255.0, 0.0, 0.0)
Color.create from list -> rgb: (10.0, 20.0, 30.0)
Color.create from DefaultColor -> rgb: (0.0, 0.0, 0.0)
"""

from colorcode import color_parser
from colorcode import color
from colorcode.default_colors import DefaultColor

# Parse a hex string into components
hex_color = "#1d4ade"
print("parse_hex_string:", color_parser.parse_hex_string(hex_color))

# Parse rgb/rgba strings
print("parse_color_string (rgb):", color_parser.parse_color_string("rgb(255,0,128)"))
print(
    "parse_color_string (rgba):", color_parser.parse_color_string("rgba(255,0,128,64)")
)

# Parse packed integer values (RGB and RGBA)
print("parse_color_int (RGB):", color_parser.parse_color_int(0x1D4ADE))
print("parse_color_int (RGBA):", color_parser.parse_color_int(0x1D4ADEEB))

# Use Color.create which accepts ints, strings, sequences and DefaultColor
print("Color.create from int -> rgb:", color.Color.create(0xFFFFFF).rgb)
print("Color.create from string -> rgb:", color.Color.create("rgb(255,0,0)").rgb)
print("Color.create from list -> rgb:", color.Color.create([10, 20, 30]).rgb)
print(
    "Color.create from DefaultColor -> rgb:", color.Color.create(DefaultColor.Black).rgb
)
