"""
File: colorcode/color_model/rgb_model.py
Description: Implementation of RGB color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ColorTriple


class RGB_Model(ColorModel):
    """
    Pass through/default color model.
    """

    def to_rgb(self, red: float, green: float, blue: float) -> ColorTriple:
        return red, green, blue

    def from_rgb(self, red: float, green: float, blue: float) -> ColorTriple:
        self.validate_rgb(red, green, blue)
        return red, green, blue
