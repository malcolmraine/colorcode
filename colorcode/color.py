from __future__ import annotations

import colorsys
from functools import singledispatch
from . import color_model
from . import color_parser


class Color(object):
    def __init__(
        self,
        r: int | float = 0,
        g: int | float = 0,
        b: int | float = 0,
        a: int | float = 0,
        base: int | float = 255,
    ) -> None:
        """
        Create a Color.

        Parameters
        ----------
        r : int | float
            The red component of the color.
        g : int | float
            The green component of the color.
        b : int | float
            The blue component of the color.
        a : int | float
            The alpha component of the color.
        base : int | float
            The maximum value for any given component value.
        """
        # All components are stored as a value between 0 and 1
        self.red = r / base
        self.green = g / base
        self.blue = b / base
        self.alpha = a / base
        self._base = base

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(r={self.red}, g={self.green}, b={self.blue}, a={self.alpha})"

    @property
    def base(self) -> int | float:
        return self._base

    @base.setter
    def base(self, base: int | float) -> None:
        self._base = base

    @property
    def rgb(self) -> tuple[float, float, float]:
        """
        Get the color as Red, Green, and Blue components.

        Returns
        -------
        tuple[float, float, float]

        """
        return self.red * self._base, self.green * self._base, self.blue * self._base

    @rgb.setter
    def rgb(self, value: tuple[float, float, float]) -> None:
        """
        Set the color as Red, Green, and Blue components.

        Parameters
        ----------
        value : tuple[float, float, float]
            The Red, Green, and Blue components of the color.

        Returns
        -------
        None

        """
        self.red = value[0] / self._base
        self.green = value[1] / self._base
        self.blue = value[2] / self._base

    @property
    def rgba(self) -> tuple[float, float, float, float]:
        return (
            self.red * self._base,
            self.green * self._base,
            self.blue * self._base,
            self.alpha,
        )

    @rgba.setter
    def rgba(self, value: tuple[float, float, float, float]) -> None:
        self.red = value[0] / self._base
        self.green = value[1] / self._base
        self.blue = value[2] / self._base
        self.alpha = value[3] / self._base

    @property
    def hsv(self) -> tuple[float, float, float]:
        """
        Get the color as Hue, Saturation, and Value components.

        Returns
        -------
        tuple[float, float, float]
            The Hue, Saturation, and Value components of the color.
            Hue is expressed as an angular value from 0-360 while Saturation and
            Value are expressed as percentages from 0-100

        """
        h, s, v = color_model.HSV_Model().from_rgb(self.red, self.green, self.blue)
        return h * 360, s * 100, s * 100

    @hsv.setter
    def hsv(self, value: tuple[float, float, float]) -> None:
        """
        Set the color as Hue, Saturation, and Value components.

        Parameters
        ----------
        value : tuple[float, float, float]
            The Hue, Saturation, and Value components of the color.
            Hue is expressed as an angular value from 0-360 while Saturation and
            Value are expressed as percentages from 0-100

        Returns
        -------
        None
        """
        h, s, v = value[0] / 360, value[1] / 100, value[2] / 100
        self.red, self.green, self.blue = map(
            int, color_model.HSV_Model().to_rgb(h, s, v)
        )

    @property
    def tsl(self) -> tuple[float, float, float]:
        """
        Get the color as Tint, Saturation, and Lightness

        Returns
        -------
        tuple[float, float, float]
        """
        tint, saturation, lightness = color_model.TSL_Model().from_rgb(
            self.red, self.green, self.blue
        )
        return tint, saturation, lightness

    @tsl.setter
    def tsl(self, value: tuple[float, float, float]) -> None:
        self.red, self.green, self.blue = color_model.TSL_Model().to_rgb(*value)

    @property
    def yiq(self) -> tuple[float, float, float]:
        """
        Get the color as Luma, In-Phase, and Quadrature components.

        Returns
        -------
        tuple[float, float, float]

        """
        return color_model.YIQ_Model().from_rgb(self.red, self.green, self.blue)

    @yiq.setter
    def yiq(self, value: tuple[float, float, float]) -> None:
        self.red, self.green, self.blue = colorsys.rgb_to_yiq(*value)

    @property
    def hls(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hls(self.red, self.green, self.blue)

    @hls.setter
    def hls(self, value: tuple[float, float, float]) -> None:
        self.red, self.green, self.blue = colorsys.rgb_to_hls(*value)

    @classmethod
    def create(cls, data: int | str | list[int]) -> Color:
        if isinstance(data, int):
            components = color_parser.parse_color_int(data)
            return cls(*components)
        elif isinstance(data, str):
            components = color_parser.parse_color_string(data)
            return cls(*components)
        else:
            return cls(*data)

    def red_chromacity(self) -> float:
        return color_model.calc_red_chromacity(self.red, self.green, self.blue)

    def green_chromacity(self) -> float:
        return color_model.calc_green_chromacity(self.red, self.green, self.blue)

    def saturation(self) -> float:
        """
        Get the saturation component of the color.

        Returns
        -------
        float
            The saturation component.

        Notes
        -----
        This converts the color to the HSV color space first.

        """
        return self.hsv[1]

    def hue(self) -> float:
        """
        Get the hue component of the color.

        Returns
        -------
        float
            The hue component of the color.

        Notes
        -----
        This converts the color to the HSV color space first.

        """
        return self.hsv[0]

    def tint(self) -> float:
        """
        Get the tint component of the color.

        Returns
        -------
        float
            The tint component of the color.

        """
        return self.tsl[0]

    def lighter(self, amount: float = 0.1) -> Color:
        """
        Make the color lighter.

        Parameters
        ----------
        amount : float
            The amount to make the color lighter.

        Returns
        -------
        Color
            The Color instance.

        Notes
        -----
        This operates on the Color instance in-place.
        """
        h, s, v = self.hsv
        s = min(0.0, s - amount)
        self.hsv = h, s, v

        return self

    def darker(self, amount: float = 0.1) -> Color:
        """
        Make the color darker.

        Parameters
        ----------
        amount : float
            The amount to make the color darker.

        Returns
        -------
        Color
            The Color instance.

        Notes
        -----
        This operates on the Color instance in-place.
        """
        h, s, v = self.hsv
        v = min(0.0, v - amount)
        self.hsv = h, s, v
        return self

    def opacity(self) -> float:
        return self.alpha
