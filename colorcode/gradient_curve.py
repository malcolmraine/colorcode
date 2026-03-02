"""
Curves for specifying the transition between the start and end of a color gradient.
"""

import math
from abc import abstractmethod, ABC

from ._util import clamp


###############################################################################
class GradientCurve(ABC):
    @abstractmethod
    def __call__(self, x: float) -> float: ...

    @staticmethod
    def _clamp(x: float) -> float:
        return clamp(x, 0, 1)


###############################################################################
class LinearCurve(GradientCurve):
    def __call__(self, x: float) -> float:
        return self._clamp(self._clamp(x))


###############################################################################
class ExponentialCurve(GradientCurve):
    def __init__(self, exponent: float = 2.0):
        self._exponent = exponent

    def __call__(self, x: float) -> float:
        return self._clamp(self._clamp(x) ** self._exponent)


###############################################################################
class LogarithmicCurve(GradientCurve):
    def __init__(self, factor=0.5) -> None:
        self._factor = factor

    def __call__(self, x: float) -> float:
        if x <= 0.0:
            return 0.0
        return self._clamp(self._factor * math.log(self._clamp(x)) + 1)
