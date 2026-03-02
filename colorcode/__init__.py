"""
File: colorcode/__init__.py
Description: Package initializer exposing major classes and submodules.
Author: Malcolm Hall
License: MIT
"""

from .color import Color
from . import color_model
from . import color_parser
from .default_colors import DefaultColor
from . import gradient
from .gradient import Gradient
from .gradient_curve import (
    GradientCurve,
    LinearCurve,
    LogarithmicCurve,
    ExponentialCurve,
)

__version__ = "0.1.0"

__all__ = [
    "Color",
    "color_model",
    "color_parser",
    "DefaultColor",
    "gradient",
    "Gradient",
    "GradientCurve",
    "LinearCurve",
    "LogarithmicCurve",
    "ExponentialCurve",
]


# Roadmap
"""
Functions to handle chroma, hue, brightness, etc
conversions to different color spaces
Conversions from grayscale to rgb
Gradient calculations
general utilities for parsing color descriptor strings.
List of default colors to choose from

"""
