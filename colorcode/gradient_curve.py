"""
File: colorcode/gradient_curve.py
Description: Curves for specifying the transition between the start and end of a color gradient.
Author: Malcolm Hall
License: MIT
"""

import math
from abc import abstractmethod, ABC

from ._util import clamp


###############################################################################
class GradientCurve(ABC):
    def __call__(self, x: float) -> float:
        return self.get_curve_value(self._clamp(x))

    @staticmethod
    def _clamp(x: float) -> float:
        return clamp(x, 0, 1)

    @abstractmethod
    def get_curve_value(self, x: float) -> float: ...


###############################################################################
class LinearCurve(GradientCurve):
    def get_curve_value(self, x: float) -> float:
        return x


###############################################################################
class ExponentialCurve(GradientCurve):
    def __init__(self, exponent: float = 2.0):
        self._exponent = exponent

    def get_curve_value(self, x: float) -> float:
        return self._clamp(x**self._exponent)


###############################################################################
class LogarithmicCurve(GradientCurve):
    def __init__(self, factor: float = 0.5) -> None:
        self._factor = factor

    def get_curve_value(self, x: float) -> float:
        if x <= 0.0:
            return 0.0
        return self._clamp(self._factor * math.log(x) + 1)
