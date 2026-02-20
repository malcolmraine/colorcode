from .color import Color
import color_model
import color_parser

__version__ = "0.1.0"

__all__ = ["Color", "color_model", "color_parser"]


# Roadmap
"""
Functions to handle chroma, hue, brightness, etc
conversions to different color spaces
Conversions from grayscale to rgb
Gradient calculations
general utilities for parsing color descriptor strings.
List of default colors to choose from

"""

# Structure
"""
A color is an instance of a class that has general methods for interacting with colors. 
A color instance should be able to easily produce values for different aspects of the color
    - hue, red, green, blue
    - Should be able to change the transparency of the color
    
A color instance has a property for its color model.
"""
