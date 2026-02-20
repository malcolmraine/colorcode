from .color import Color
from . import color_model
from . import color_parser
from .default_colors import DefaultColors

__version__ = "0.1.0"

__all__ = ["Color", "color_model", "color_parser", "DefaultColors"]


# Roadmap
"""
Functions to handle chroma, hue, brightness, etc
conversions to different color spaces
Conversions from grayscale to rgb
Gradient calculations
general utilities for parsing color descriptor strings.
List of default colors to choose from

"""
