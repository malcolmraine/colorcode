"""
File: colorcode/color_model/rgb_model.py
Description: Implementation of RGB color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ModelTuple
import colorsys


class HSL_Model(ColorModel):
    def to_rgb(self, hue: float, saturation: float, lightness: float) -> ModelTuple:
        # colorsys expects arguments in HLS order (hue, lightness, saturation).
        # our method signature names the second and third parameters
        # ``saturation`` and ``lightness`` respectively, so swap them when
        # invoking the underlying conversion to match the expected order.
        return colorsys.hls_to_rgb(hue, lightness, saturation)

    def from_rgb(self, red: float, green: float, blue: float) -> ModelTuple:
        # ``colorsys.rgb_to_hls`` returns (hue, lightness, saturation).
        # we convert to the external (hue, saturation, lightness) ordering
        # so rename the middle component to avoid an ambiguous `l` name.
        h, lightness, s = colorsys.rgb_to_hls(red, green, blue)
        return h, s, lightness
