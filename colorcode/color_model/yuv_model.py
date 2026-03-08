"""
File: colorcode/color_model/yuv_model.py
Description: Implementation of Y'UV color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ModelTuple
from ..util import clamp
from typing import Final
import enum


U_MAX: Final[float] = 0.436
V_MAX: Final[float] = 0.615


class YUVStandard(enum.StrEnum):
    BT470 = "BT.470"
    BT709 = "BT.709"


class YUV_Model(ColorModel):
    def __init__(self, standard: YUVStandard) -> None:
        super().__init__()
        match standard:
            case YUVStandard.BT470:
                self._wr = 0.299
                self._wb = 0.114
                self._wg = 0.587
            case YUVStandard.BT709:
                self._wr = 0.2126
                self._wb = 0.7152
                self._wg = 0.0722
            case _:
                raise ValueError(f"Unknown standard: {standard}")

    def to_rgb(self, y: float, u: float, v: float) -> ModelTuple:
        red = y + v * ((1 - self._wr) / V_MAX)
        green = (
            y
            - ((u * (self._wb - self._wb**2)) / (U_MAX * self._wg))
            - ((v * (self._wr - self._wr**2)) / (V_MAX * self._wg))
        )
        blue = y + u * ((1 - self._wb) / U_MAX)

        return clamp(red, 0, 1), clamp(green, 0, 1), clamp(blue, 0, 1)

    def from_rgb(self, red: float, green: float, blue: float) -> ModelTuple:
        y = self._wr * red + self._wg * green + self._wb * blue
        u = U_MAX * ((blue - y) / (1 - self._wb))
        v = V_MAX * ((red - y) / (1 - self._wr))
        return clamp(y, 0, 1), clamp(u, -U_MAX, U_MAX), clamp(v, -V_MAX, V_MAX)
