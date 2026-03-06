"""
File: colorcode/color_model/rgb_model.py
Description: Implementation of RGB color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ModelTuple


class RGB_Model(ColorModel):
    """
    Pass through/default color model.
    """

    def to_rgb(self, red: float, green: float, blue: float) -> ModelTuple:
        return red, green, blue

    def from_rgb(self, red: float, green: float, blue: float) -> ModelTuple:
        return red, green, blue
