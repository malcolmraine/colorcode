"""
File: colorcode/color_model/tsl_model.py
Description: Implementation of TSL color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ColorTriple
from .. import util

import math


class TSL_Model(ColorModel):
    def to_rgb(self, tint: float, saturation: float, lightness: float) -> ColorTriple:
        x = math.tan(math.tau * (float(tint) - 0.25)) ** 2
        r_prime = math.sqrt((5 * float(saturation) ** 2) / (9 * ((x**-1) + 1)))
        g_prime = math.sqrt((5 * float(saturation) ** 2) / (9 * (x + 1)))
        r = r_prime + (1.0 / 3.0)
        g = g_prime + (1.0 / 3.0)
        k = lightness / (0.185 * r + 0.473 * g + 0.114)
        red = k * r
        green = k * g
        blue = k * (1 - r - g)

        return red, green, blue

    def from_rgb(self, red: float, green: float, blue: float) -> ColorTriple:
        self.validate_rgb(red, green, blue)

        r_prime = util.calc_red_chromacity(red, green, blue) - (1.0 / 3.0)
        g_prime = util.calc_green_chromacity(red, green, blue) - (1.0 / 3.0)

        if g_prime != 0:
            tint = 0.5 - (math.atan2(g_prime, r_prime) / math.tau)
        else:
            tint = 0

        saturation = math.sqrt((9 / 5) * (r_prime**2 + g_prime**2))
        lightness = (red * 0.299) + (green * 0.587) + (blue * 0.114)
        return tint, saturation, lightness
