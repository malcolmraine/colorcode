"""
File: colorcode/color_model/hsv_model.py
Description: Implementation of HSV color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ColorTriple

import colorsys


class HSV_Model(ColorModel):
    def to_rgb(self, hue: float, saturation: float, value: float) -> ColorTriple:
        return colorsys.hsv_to_rgb(hue, saturation, value)

    def from_rgb(self, red: float, green: float, blue: float) -> ColorTriple:
        self.validate_rgb(red, green, blue)
        return colorsys.rgb_to_hsv(red, green, blue)
