"""
File: colorcode/color_model/base_model.py
Description: Base class for color model implementations.
Author: Malcolm Hall
License: MIT
"""

from __future__ import annotations

from abc import abstractmethod, ABC


ModelTuple = tuple[float, float, float]


class ColorModel(ABC):
    @abstractmethod
    def to_rgb(self, a: float, b: float, c: float) -> ModelTuple: ...

    @abstractmethod
    def from_rgb(self, red: float, green: float, blue: float) -> ModelTuple: ...
