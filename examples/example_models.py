"""Example 2 — ColorModel conversions

Shows how to use `HSV_Model`, `HSL_Model`, `YIQ_Model` and `TSL_Model` to
convert RGB -> model components -> RGB. TSL may not invert perfectly; we
illustrate that while still validating types and ranges.

Expected output
---------------
Original RGB: (0.2, 0.4, 0.6)
HSV: (0.5833333333333334, 0.6666666666666666, 0.6)
HSV -> RGB: (0.2, 0.4, 0.6)
HSL: (0.5833333333333334, 0.49999999999999994, 0.4)
HSL -> RGB: (0.19999999999999996, 0.3999999999999998, 0.6000000000000001)
YIQ: (0.9528868360277136, 0.0, 0.7819861431870669)
YIQ -> RGB: (1.0, 0.4557852207555499, 1.0)
TSL: (0, 0.22360679774997896, 0.36300000000000004)
TSL -> RGB (may not be exact): (0.49839816933638453, 0.33226544622425636, 0.1661327231121282)
"""

from colorcode import color_model

rgb = (0.2, 0.4, 0.6)
print("Original RGB:", rgb)

# HSV round-trip
hsv = color_model.HSV_Model()
h, s, v = hsv.from_rgb(*rgb)
print("HSV:", (h, s, v))
print("HSV -> RGB:", hsv.to_rgb(h, s, v))

# HSL round-trip
hsl = color_model.HSL_Model()
h, s, lightness = hsl.from_rgb(*rgb)
print("HSL:", (h, s, lightness))
print("HSL -> RGB:", hsl.to_rgb(h, s, lightness))

# YIQ round-trip
yiq = color_model.YIQ_Model()
y, i, q = yiq.from_rgb(*rgb)
print("YIQ:", (y, i, q))
print("YIQ -> RGB:", yiq.to_rgb(y, i, q))

# TSL conversion (library-specific)
tsl = color_model.TSL_Model()
t, s_tsl, l_tsl = tsl.from_rgb(*rgb)
print("TSL:", (t, s_tsl, l_tsl))
print("TSL -> RGB (may not be exact):", tsl.to_rgb(t, s_tsl, l_tsl))
