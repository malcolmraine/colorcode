"""
File: colorcode/_color_types.py
Description: Shared type aliases used across the package.
Author: Malcolm Hall
License: MIT
"""

# Components may be ints (0-255) or floats (0.0-1.0) depending on context.
Component = float | int

ComponentTuple = (
    tuple[Component, Component, Component]
    | tuple[Component, Component, Component, Component]
)
