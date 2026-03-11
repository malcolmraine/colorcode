"""
File: colorcode/gradient/__init__.py
Description: Gradient calculations between two colors.
Author: Malcolm Hall
License: MIT
"""

from .gradient import Gradient
from .gradient_curve import (
    GradientCurve,
    LinearCurve,
    ExponentialCurve,
    LogarithmicCurve,
    AgnesiWitchCurve,
    TriangleCurve,
    RandomCurve,
)

__all__ = [
    "Gradient",
    "GradientCurve",
    "LinearCurve",
    "ExponentialCurve",
    "LogarithmicCurve",
    "AgnesiWitchCurve",
    "TriangleCurve",
    "RandomCurve",
]
