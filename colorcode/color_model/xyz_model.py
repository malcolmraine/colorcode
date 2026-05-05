"""
File: colorcode/color_model/xyz_model.py
Description: Implementation of XYZ color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ColorTriple
from .. import util
import numpy as np


class XYZ_Model(ColorModel):
    def to_rgb(self, x: float, y: float, z: float) -> ColorTriple:
        """
        Convert CIE XYZ to sRGB.

        The XYZ to linear RGB conversion uses the inverse of the standard RGB to XYZ
        transformation matrix (D65 illuminant, assuming 2° standard observer):

        [R']     [  3.2404542  -1.5371385  -0.4985314] [X]
        [G']  =  [ -0.9692660   1.8760108   0.0415560] [Y]
        [B']     [  0.0556434  -0.2040259   1.0572252] [Z]

        The linear RGB values are then converted to sRGB using the companding function.
        """
        self.validate_rgb(x, y, z)

        # Inverse transformation matrix (XYZ to linear RGB)
        inverse_matrix = np.array(
            [
                [3.2404542, -1.5371385, -0.4985314],
                [-0.9692660, 1.8760108, 0.0415560],
                [0.0556434, -0.2040259, 1.0572252],
            ]
        )

        xyz = np.array([x, y, z])
        linear_rgb = inverse_matrix @ xyz

        # Convert from linear RGB to sRGB using companding
        red = self._linear_to_srgb(linear_rgb[0])
        green = self._linear_to_srgb(linear_rgb[1])
        blue = self._linear_to_srgb(linear_rgb[2])

        return red, green, blue

    def from_rgb(self, red: float, green: float, blue: float) -> ColorTriple:
        """
        Convert sRGB values to CIE XYZ.

        The sRGB values are first converted to linear RGB using inverse companding.
        Then, the linear RGB is transformed to XYZ using the standard transformation
        matrix (D65 illuminant, 2° standard observer):

        [X]     [0.4124564  0.3575761  0.1804375] [R']
        [Y]  =  [0.2126729  0.7151522  0.0721750] [G']
        [Z]     [0.0193339  0.1191920  0.9503041] [B']

        where R', G', B' are linear RGB values.
        """
        self.validate_rgb(red, green, blue)

        # Convert from sRGB to linear RGB using inverse companding
        linear_red = self._srgb_to_linear(red)
        linear_green = self._srgb_to_linear(green)
        linear_blue = self._srgb_to_linear(blue)

        transformation_matrix = np.array(
            [
                [0.4124564, 0.3575761, 0.1804375],
                [0.2126729, 0.7151522, 0.0721750],
                [0.0193339, 0.1191920, 0.9503041],
            ]
        )

        linear_rgb = np.array([linear_red, linear_green, linear_blue])
        xyz = transformation_matrix @ linear_rgb

        return tuple(float(v) for v in xyz)

    @staticmethod
    def _srgb_to_linear(value: float) -> float:
        """Convert a single sRGB value to linear RGB."""
        if value <= 0.04045:
            return value / 12.92
        else:
            return ((value + 0.055) / 1.055) ** 2.4

    @staticmethod
    def _linear_to_srgb(value: float) -> float:
        """Convert a single linear RGB value to sRGB."""
        if value <= 0.0031308:
            return 12.92 * value
        else:
            return (1.055 * (value ** (1 / 2.4))) - 0.055
