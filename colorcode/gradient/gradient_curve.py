"""
File: colorcode/gradient_curve.py
Description: Curves for specifying the transition between the start and end of a color gradient.
Author: Malcolm Hall
License: MIT
"""

import math
import random
from abc import abstractmethod, ABC
import typing
from colorcode.util import clamp


###############################################################################
class GradientCurve(ABC):
    def __call__(self, x: float) -> float:
        return self._clamp(self.get_curve_value(self._clamp(x)))

    @staticmethod
    def _clamp(x: float) -> float:
        return clamp(x, 0, 1)

    @abstractmethod
    def get_curve_value(self, x: float) -> float: ...


###############################################################################
class LinearCurve(GradientCurve):
    @typing.override
    def get_curve_value(self, x: float) -> float:
        return x


###############################################################################
class ExponentialCurve(GradientCurve):
    def __init__(self, exponent: float = 2.0):
        self._exponent = exponent

    @typing.override
    def get_curve_value(self, x: float) -> float:
        return float(x**self._exponent)


###############################################################################
class LogarithmicCurve(GradientCurve):
    def __init__(self, factor: float = 0.5) -> None:
        self._factor = factor

    @typing.override
    def get_curve_value(self, x: float) -> float:
        if x <= 0.0:
            return 0.0
        return self._factor * math.log(x) + 1


###############################################################################
class AgnesiWitchCurve(GradientCurve):
    """
    Modified version of the Witch of Agnesi function.
    Basically looks like a narrow bell curve.
    """

    def __init__(self, factor: float = 0.04) -> None:
        self._factor = factor

    @typing.override
    def get_curve_value(self, x: float) -> float:
        return float(
            (8 * (self._factor**2.2154)) / ((x - 0.5) ** 2 + (4 * self._factor**2))
        )


###############################################################################
class TriangleCurve(GradientCurve):
    """
    Generates a curve shaped like a triangle. The maximum Y value is at x=0.5
    """

    @typing.override
    def get_curve_value(self, x: float) -> float:
        if 0 <= x <= 0.5:
            return x * 2
        return (1 - 2 * x) + 1


###############################################################################
class RandomCurve(GradientCurve):
    """
    Generate random curve values.
    """

    def __init__(
        self,
        step: float = 0.001,
        seed: int | float | str | bytes | bytearray | None = None,
    ) -> None:
        """
        Initialize the random curve generator.

        Parameters
        ----------
        step : float
            Step size for the curve. This should be a number between 0 and 1.
        seed : int | float | str | bytes| bytearray | None
            Seed for the random number generator. If None, the default seed from the
            random library is used.
        """
        self._generator = random.Random()
        self._step = step
        self._generator.seed(seed)
        self._end = int(1 / step)

    @typing.override
    def get_curve_value(self, x: float) -> float:
        return random.randrange(0, self._end) * self._step
