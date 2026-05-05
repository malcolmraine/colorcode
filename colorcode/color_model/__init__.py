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
from .yuv_model import YUV_Model, YUVStandard
from .ydbdr_model import YDbDr_Model
from .xyz_model import XYZ_Model
from .cielab_model import CIELAB_Model
import enum


class ColorModelType(enum.StrEnum):
    HSV = "HSV"
    RGB = "RGB"
    TSL = "TSL"
    HSL = "HSL"
    YIQ = "YIQ"
    YUV_BT470 = "YUV_BT470"
    YUV_BT709 = "YUV_BT709"
    YDbDr = "YDbDr"
    XYZ = "XYZ"
    CIELAB = "CIELAB"


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
        case ColorModelType.YUV_BT470:
            return YUV_Model(YUVStandard.BT470)
        case ColorModelType.YUV_BT709:
            return YUV_Model(YUVStandard.BT709)
        case ColorModelType.YDbDr:
            return YDbDr_Model()
        case ColorModelType.XYZ:
            return XYZ_Model()
        case ColorModelType.CIELAB:
            return CIELAB_Model()
        case _:
            raise ValueError(f"Unknown color model type: {model_type}")
