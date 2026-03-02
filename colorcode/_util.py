"""
File: colorcode/_util.py
Description: Utility helpers used internally by the package.
Author: Malcolm Hall
License: MIT
"""


def clamp(value: float | int, lower: float | int, upper: float | int) -> float | int:
    return min(max(value, lower), upper)
