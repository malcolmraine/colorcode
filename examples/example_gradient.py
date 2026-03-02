"""Example 3 — Gradients & curves

Demonstrates creating a `Gradient`, iterating steps, using `get_color()` at
fractions, and applying an `ExponentialCurve` to change easing.

Expected output
---------------
Linear gradient steps:
(204.0, 0.0, 51.0)
(153.0, 0.0, 102.0)
(102.0, 0.0, 153.0)
(51.0, 0.0, 204.0)
(0.0, 0.0, 255.0)
Midpoint (50%): (127.5, 0.0, 127.5)
Exponential curve gradient steps:
(250.43842132590044, 0.0, 4.561578674099572)
(229.19581429302602, 0.0, 25.80418570697398)
(183.89202576363184, 0.0, 71.10797423636816)
(109.02948242881371, 0.0, 145.9705175711863)
(0.0, 0.0, 255.0)
"""

from colorcode import color, gradient
from colorcode.gradient_curve import ExponentialCurve

start = color.Color(255, 0, 0)  # red
end = color.Color(0, 0, 255)  # blue

# Linear gradient with 5 steps
g = gradient.Gradient(start, end, steps=5)
print("Linear gradient steps:")
for c in g:
    print(c.rgb)

# Get color at specific fraction (50%)
g2 = gradient.Gradient(start, end, steps=10)
mid = g2.get_color(0.5)
print("Midpoint (50%):", mid.rgb)

# Use an exponential easing curve to emphasize the start
exp_curve = ExponentialCurve(exponent=2.5)
g_exp = gradient.Gradient(start, end, curve=exp_curve, steps=5)
print("Exponential curve gradient steps:")
for c in g_exp:
    print(c.rgb)
