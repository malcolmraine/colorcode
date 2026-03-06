"""
File: colorcode/color_model.py
Description: Implementations of various colour models (RGB, HSV, HSL, TSL, YIQ) and conversion routines between them.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel
from .hsv_model import HSV_Model
from .hsl_model import HSL_Model
from .tsl_model import TSL_Model
from .yiq_model import YIQ_Model
from .rgb_model import RGB_Model
import enum


class ColorModelType(enum.StrEnum):
    HSV = "HSV"
    RGB = "RGB"
    TSL = "TSL"
    HSL = "HSL"
    YIQ = "YIQ"


def create(model_type: ColorModelType) -> ColorModel:
    match model_type:
        case ColorModelType.HSV:
            return HSV_Model()
        case ColorModelType.RGB:
            return RGB_Model()
        case ColorModelType.TSL:
            return TSL_Model()
        case ColorModelType.HSL:
            return HSL_Model()
        case ColorModelType.YIQ:
            return YIQ_Model()
        case _:
            raise ValueError(f"Unknown color model type: {model_type}")
