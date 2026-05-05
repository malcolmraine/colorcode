"""
File: colorcode/color_model/cielab_model.py
Description: Implementation of L*a*b* color model.
Author: Malcolm Hall
License: MIT
"""

from .base_model import ColorModel, ColorTriple
from . import xyz_model
import math


class CIELAB_Model(ColorModel):
    # D65 standard illuminant XYZ values for 2° observer
    _D65_XN = 0.95047
    _D65_YN = 1.00000
    _D65_ZN = 1.08883

    # Delta value for the piecewise L*a*b* transformation
    _DELTA = 6 / 29

    def to_rgb(self, L: float, a: float, b: float) -> ColorTriple:
        """
        Convert CIE L*a*b* to sRGB.

        The conversion is a two-step process:
        1. L*a*b* → XYZ using the inverse of the nonlinear transformation
        2. XYZ → sRGB using the standard inverse transformation matrix

        The L*a*b* to XYZ conversion uses:

        Fy = (L* + 16) / 116
        Fx = a*/500 + Fy
        Fz = Fy - b*/200

        Then XYZ is recovered using the piecewise function:
        if F > δ: f³ = value
        else: f = (3δ²)(F - 4/29)

        where X = Xn * f(Fx), Y = Yn * f(Fy), Z = Zn * f(Fz)
        """
        # Convert L*a*b* to XYZ
        fy = (L + 16) / 116
        fx = a / 500 + fy
        fz = fy - b / 200

        # Apply inverse piecewise function
        x = self._CIELAB_to_XYZ_component(fx) * self._D65_XN
        y = self._CIELAB_to_XYZ_component(fy) * self._D65_YN
        z = self._CIELAB_to_XYZ_component(fz) * self._D65_ZN

        # Convert XYZ to RGB
        xyz_model_inst = xyz_model.XYZ_Model()
        return xyz_model_inst.to_rgb(x, y, z)

    def from_rgb(self, red: float, green: float, blue: float) -> ColorTriple:
        """
        Convert sRGB values to CIE-L*a*b*.

        The conversion is a two-step process:
        1. sRGB → XYZ using the standard transformation matrix
        2. XYZ → L*a*b* using the nonlinear transformation

        The XYZ to L*a*b* conversion uses:

        Fx = f(X/Xn), Fy = f(Y/Yn), Fz = f(Z/Zn)

        where f is the piecewise function:
        if value > δ³: f = value^(1/3)
        else: f = value/(3δ²) + 4/29

        Then:
        L* = 116*Fy - 16
        a* = 500*(Fx - Fy)
        b* = 200*(Fy - Fz)

        where δ = 6/29
        """
        self.validate_rgb(red, green, blue)

        # Convert sRGB to XYZ
        xyz_model_inst = xyz_model.XYZ_Model()
        x, y, z = xyz_model_inst.from_rgb(red, green, blue)

        # Normalize by D65 illuminant
        fx = self._XYZ_to_CIELAB_component(x / self._D65_XN)
        fy = self._XYZ_to_CIELAB_component(y / self._D65_YN)
        fz = self._XYZ_to_CIELAB_component(z / self._D65_ZN)

        # Calculate L*a*b*
        L = 116 * fy - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)

        return L, a, b

    def _XYZ_to_CIELAB_component(self, value: float) -> float:
        """
        Apply the nonlinear transformation for XYZ to L*a*b*.
        
        Uses the piecewise function from CIE standard.
        """
        delta_cubed = self._DELTA ** 3
        if value > delta_cubed:
            return value ** (1 / 3)
        else:
            return value / (3 * self._DELTA ** 2) + 4 / 29

    def _CIELAB_to_XYZ_component(self, value: float) -> float:
        """
        Apply the inverse nonlinear transformation for L*a*b* to XYZ.
        
        Uses the inverse of the piecewise function from CIE standard.
        """
        if value > self._DELTA:
            return value ** 3
        else:
            return 3 * (self._DELTA ** 2) * (value - 4 / 29)
