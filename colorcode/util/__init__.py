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


def intensity_from_srgb(
    red: float, green: float, blue: float
) -> tuple[float, float, float]:
    """
    
    Parameters
    ----------
    red
    green
    blue

    Returns
    -------

    """
    if red <= 0.04045:
        red_intensity = red / 12.92
    else:
        red_intensity = ((red + 0.055) / 1.055) ** 2.4

    if green <= 0.04045:
        green_intensity = green / 12.92
    else:
        green_intensity = ((green + 0.055) / 1.055) ** 2.4

    if blue <= 0.04045:
        blue_intensity = blue/ 12.92
    else:
        blue_intensity = ((blue + 0.055) / 1.055) ** 2.4

    return red_intensity, green_intensity, blue_intensity


def intensity_to_srgb(red_intensity: float, green_intensity: float, blue_intensity: float) -> tuple[float, float, float]:
    if red_intensity <= 0.0031308:
        red = 12.92 * red_intensity
    else:
        red = (1.055 * red_intensity ** (1/2.4)) - 0.055

    if green_intensity <= 0.0031308:
        green = 12.92 * green_intensity
    else:
        green = (1.055 * green_intensity ** (1/2.4)) - 0.055

    if blue_intensity <= 0.0031308:
        blue = 12.92 * blue_intensity
    else:
        blue = (1.055 * (blue_intensity ** (1/2.4))) - 0.055

    return red, green, blue