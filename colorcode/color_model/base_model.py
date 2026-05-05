"""
File: colorcode/color_model/base_model.py
Description: Base class for color model implementations.
Author: Malcolm Hall
License: MIT
"""

from __future__ import annotations

from abc import abstractmethod, ABC

ColorTriple = tuple[float, float, float]


class ColorModel(ABC):
    @abstractmethod
    def to_rgb(self, *components: float) -> ColorTriple:
        """
        Convert the components of the color model to an sRGB triple.

        Parameters
        ----------
        components: float...
            The components of the color model.

        Returns
        -------
        tuple[float, float, float]
            The color model components converted to sRGB values.
        """

    @abstractmethod
    def from_rgb(self, red: float, green: float, blue: float) -> ColorTriple:
        """
        Convert R, G, B values to the components of the color model.
        Parameters
        ----------
        red : float
            Red component of the color model.
        green : float
            Green component of the color model.
        blue : float
            Blue component of the color model.

        Returns
        -------
        ColorTriple

        Notes
        -----
        The inputs are assumed to be sRGB values in the [0, 1] range.
        """

    @staticmethod
    def validate_rgb(red: float, green: float, blue: float) -> None:
        """
        Validate that the components of the color model are sRGB values.

        Parameters
        ----------
        red : float
            The red component of the color model.
        green : float
            The green component of the color model.
        blue : float
            The blue component of the color model.

        Raises
        -------
        ValueError
            If the components of the color model are not sRGB values in the [0, 1] range.

        """
        if red < 0 or green < 0 or blue < 0 or red > 1 or green > 1 or blue > 1:
            raise ValueError(
                "Color model conversion requires sRGB values in [0, 1] range."
            )
