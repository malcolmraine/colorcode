"""
File: colorcode/color_model/ydbdr_model.py
Description: Implementation of YDbDr color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ColorTriple
from ..util import clamp


class YDbDr_Model(ColorModel):
    """
    Luminance, Blue Chrominance, Red Chrominance
    """

    def to_rgb(self, y: float, d_b: float, d_r: float) -> ColorTriple:
        red = y + (0.000092303716148 * d_b) - (0.525912630661865 * d_r)
        green = y - (0.129131898890509 * d_b) + (0.267899328207599 * d_r)
        blue = y + (0.664679059978955 * d_b) - (0.000079202543533 * d_r)

        return clamp(red, 0, 1), clamp(green, 0, 1), clamp(blue, 0, 1)

    def from_rgb(self, red: float, green: float, blue: float) -> ColorTriple:
        self.validate_rgb(red, green, blue)

        y = (0.299 * red) + (0.587 * green) + (0.114 * blue)
        d_b = (-450 * red) - (0.883 * green) + (1.333 * blue)
        d_r = (-1.333 * red) + (1.116 * green) + (0.217 * blue)
        return clamp(y, 0, 1), clamp(d_b, -1.333, 1.333), clamp(d_r, -1.333, 1.333)
