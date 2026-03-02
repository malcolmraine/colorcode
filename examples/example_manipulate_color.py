"""Example 4 — Color manipulation & packing

Shows color manipulation helpers (`lighter`, `darker`, `opacity`) and how the
color packs into a 32-bit integer via `__index__()`.

Expected output
---------------
Original rgba: (100.0, 150.0, 200.0, 128.0)
Lighter rgb: (0, 0, 0)
Darker rgb: (0, 0, 0)
Opacity (normalized): 0.5019607843137255
Packed RGBA int: 1687603328
Packed hex: 0x6496c880
Red chromacity: 0.22222222222222224
Green chromacity: 0.33333333333333337
"""

from colorcode import color

c = color.Color(100, 150, 200, a=128)
print("Original rgba:", c.rgba)

# Make the color lighter and darker (in-place)
lighter = color.Color(*c.rgb)
lighter.lighter(0.2)
print("Lighter rgb:", lighter.rgb)

darker = color.Color(*c.rgb)
darker.darker(0.2)
print("Darker rgb:", darker.rgb)

# Opacity (normalized alpha)
print("Opacity (normalized):", c.opacity())

# Packed integer index (RGBA packed into 32-bit int)
packed = c.__index__()
print("Packed RGBA int:", packed)
print("Packed hex:", hex(packed))

# Chromacity values
print("Red chromacity:", c.red_chromacity())
print("Green chromacity:", c.green_chromacity())
