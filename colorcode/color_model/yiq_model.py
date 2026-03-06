"""
File: colorcode/color_model/yiq_model.py
Description: Implementation of YIQ color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ModelTuple
import colorsys


class YIQ_Model(ColorModel):
    def to_rgb(self, y: float, i: float, q: float) -> ModelTuple:
        return colorsys.yiq_to_rgb(y, i, q)

    def from_rgb(self, red: float, green: float, blue: float) -> ModelTuple:
        return colorsys.rgb_to_yiq(red, green, blue)
