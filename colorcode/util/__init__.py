"""
File: colorcode/util/__init__.py
Description: Color utility functions.
Author: Malcolm Hall
License: MIT
"""

from .colorstrip_exporter import export_colorstrip

__all__ = ["export_colorstrip", "clamp"]


def calc_red_chromacity(red: float, green: float, blue: float) -> float:
    return red / (red + blue + green)


def calc_green_chromacity(red: float, green: float, blue: float) -> float:
    return green / (red + blue + green)


def clamp(value: float | int, lower: float | int, upper: float | int) -> float | int:
    return min(max(value, lower), upper)
