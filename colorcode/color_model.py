"""
colorcode/color_model.py

Implementations of various colour models (RGB, HSV, HSL, TSL, YIQ) and
conversion routines between them.
"""

from __future__ import annotations

import colorsys
import math
from abc import abstractmethod, ABC
import enum
from ._color_types import ComponentTuple


def calc_red_chromacity(red: float, green: float, blue: float) -> float:
    return red / (red + blue + green)


def calc_green_chromacity(red: float, green: float, blue: float) -> float:
    return green / (red + blue + green)


###############################################################################
class ColorModelType(enum.StrEnum):
    HSV = "HSV"
    RGB = "RGB"
    TSL = "TSL"
    HSL = "HSL"


###############################################################################
class ColorComponent(enum.StrEnum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    HUE = "Hue"
    SATURATION = "Saturation"
    VALUE = "Value"
    LIGHTNESS = "Lightness"
    TINT = "Tint"


###############################################################################
class ColorModel(ABC):
    @abstractmethod
    def to_rgb(self, *args: float) -> ComponentTuple: ...

    @abstractmethod
    def from_rgb(self, red: float, green: float, blue: float) -> tuple[float, ...]: ...

    @classmethod
    def create(cls, model_type: ColorModelType) -> ColorModel:
        match model_type.value:
            case ColorModelType.HSV:
                return HSV_Model()
            case ColorModelType.RGB:
                return RGB_Model()
            case ColorModelType.TSL:
                return TSL_Model()
            case ColorModelType.HSL:
                return HSL_Model()
            case _:
                raise ValueError(f"Unknown color model type: {model_type.value}")


###############################################################################
class RGB_Model(ColorModel):
    """
    Pass through/default color model.
    """

    def to_rgb(self, red: float, green: float, blue: float) -> ComponentTuple:
        return red, green, blue

    def from_rgb(self, red: float, green: float, blue: float) -> ComponentTuple:
        return red, green, blue


###############################################################################
class TSL_Model(ColorModel):
    def to_rgb(
        self, tint: float, saturation: float, lightness: float
    ) -> ComponentTuple:
        x = math.tan(math.tau * (float(tint) - 0.25)) ** 2
        r_prime = math.sqrt((5 * float(saturation) ** 2) / (9 * ((x**-1) + 1)))
        g_prime = math.sqrt((5 * float(saturation) ** 2) / (9 * (x + 1)))
        r = r_prime + colorsys.ONE_THIRD
        g = g_prime + colorsys.ONE_THIRD
        k = lightness / (0.185 * r + 0.473 * g + 0.114)
        red = k * r
        green = k * g
        blue = k * (1 - r - g)

        return red, green, blue

    def from_rgb(self, red: float, green: float, blue: float) -> ComponentTuple:
        r_prime = calc_red_chromacity(red, green, blue) - colorsys.ONE_THIRD
        g_prime = calc_green_chromacity(red, green, blue) - colorsys.ONE_THIRD

        if g_prime != 0:
            tint = 0.5 - (math.atan2(g_prime, r_prime) / math.tau)
        else:
            tint = 0

        saturation = math.sqrt((9 / 5) * (r_prime**2 + g_prime**2))
        lightness = (red * 0.299) + (green * 0.587) + (blue * 0.114)
        return tint, saturation, lightness


###############################################################################
class HSV_Model(ColorModel):
    def to_rgb(self, hue: float, saturation: float, value: float) -> ComponentTuple:
        return colorsys.hsv_to_rgb(hue, saturation, value)

    def from_rgb(self, red: float, green: float, blue: float) -> ComponentTuple:
        return colorsys.rgb_to_hsv(red, green, blue)


###############################################################################
class HSL_Model(ColorModel):
    def to_rgb(self, hue: float, saturation: float, lightness: float) -> ComponentTuple:
        # colorsys expects arguments in HLS order (hue, lightness, saturation).
        # our method signature names the second and third parameters
        # ``saturation`` and ``lightness`` respectively, so swap them when
        # invoking the underlying conversion to match the expected order.
        return colorsys.hls_to_rgb(hue, lightness, saturation)

    def from_rgb(self, red: float, green: float, blue: float) -> ComponentTuple:
        h, l, s = colorsys.rgb_to_hls(red, green, blue)
        return h, s, l


###############################################################################
class YIQ_Model(ColorModel):
    def to_rgb(self, y: float, i: float, q: float) -> ComponentTuple:
        return colorsys.yiq_to_rgb(y, i, q)

    def from_rgb(self, red: float, green: float, blue: float) -> ComponentTuple:
        return colorsys.yiq_to_rgb(red, green, blue)
