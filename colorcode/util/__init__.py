"""
File: colorcode/util/__init__.py
Description: Color utility functions.
Author: Malcolm Hall
License: MIT
"""

from .colorstrip_exporter import export_colorstrip
import enum

__all__ = [
    "export_colorstrip",
    "clamp",
    "calc_red_chromacity",
    "calc_green_chromacity",
    "luma_from_rgb",
    "rgb_to_grayscale",
    "GrayscaleMethod",
    "LumaMethod",
]


def calc_red_chromacity(red: float, green: float, blue: float) -> float:
    return red / (red + blue + green)


def calc_green_chromacity(red: float, green: float, blue: float) -> float:
    return green / (red + blue + green)


def clamp(value: float | int, lower: float | int, upper: float | int) -> float | int:
    return min(max(value, lower), upper)


class LumaMethod(enum.StrEnum):
    BT601 = "Luminosity_BT.601"
    BT709 = "Luminosity_BT.709"
    SMPTE_240M = "Luminosity_SMPTE_240M"


class GrayscaleMethod(enum.StrEnum):
    AVERAGE = "Average"
    LIGHTNESS = "Lightness"
    LUMINOSITY_BT601 = "Luminosity_BT.601"
    LUMINOSITY_BT709 = "Luminosity_BT.709"
    LUMINOSITY_SMPTE_240M = "Luminosity_SMPTE_240M"


def luma_from_rgb(
    red: int | float,
    green: int | float,
    blue: int | float,
    method: LumaMethod = LumaMethod.BT709,
) -> float:
    match method:
        case LumaMethod.BT601:
            return 0.299 * red + 0.587 * green + 0.114 * blue
        case LumaMethod.BT709:
            return 0.2126 * red + 0.7152 * green + 0.0722 * blue
        case LumaMethod.SMPTE_240M:
            return 0.212 * red + 0.701 * green + 0.087 * blue
        case _:
            raise ValueError("Invalid Luma method.")


def rgb_to_grayscale(
    red: int | float,
    green: int | float,
    blue: int | float,
    method: GrayscaleMethod = GrayscaleMethod.LIGHTNESS,
) -> float:
    match method:
        case GrayscaleMethod.LIGHTNESS:
            return (max(red, green, blue) + min(red, green, blue)) / 2.0
        case GrayscaleMethod.LIGHTNESS:
            return (red + green + blue) / 3
        case GrayscaleMethod.LUMINOSITY_BT601:
            return luma_from_rgb(red, green, blue, LumaMethod.BT601)
        case GrayscaleMethod.LUMINOSITY_BT709:
            return luma_from_rgb(red, green, blue, LumaMethod.BT709)
        case GrayscaleMethod.LUMINOSITY_SMPTE_240M:
            return luma_from_rgb(red, green, blue, LumaMethod.SMPTE_240M)
        case _:
            raise ValueError("Invalid method provided.")
