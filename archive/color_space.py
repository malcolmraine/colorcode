from __future__ import annotations
import abc
import colorsys
import math
import typing

import color_types
from colorcode.color_types import ComponentValue


###############################################################################
class ColorSpace(abc.ABC):
    @classmethod
    def from_rgb[T](cls: T, model: ColorSpace_RGB) -> T: ...

    @abc.abstractmethod
    def to_rgb(self) -> ColorSpace_RGB: ...


###############################################################################
class ColorSpace_RGB(ColorSpace):
    """
    Red, Green, and Blue

    References
    ----------
    https://en.wikipedia.org/wiki/RGB_color_spaces
    """

    def __init__(
        self,
        red: float | int | color_types.ComponentValue = 0.0,
        green: float | int | color_types.ComponentValue = 0.0,
        blue: float | int | color_types.ComponentValue = 0.0,
        alpha: float | int | color_types.ComponentValue = 0.0,
    ):
        self.red = color_types.ComponentValue(red)
        self.green = color_types.ComponentValue(green)
        self.blue = color_types.ComponentValue(blue)
        self.alpha = color_types.ComponentValue(alpha)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(red={self.red}, green={self.green}, blue={self.blue}, alpha={self.alpha})"

    def __copy__(self):
        return ColorSpace_RGB(self.red, self.green, self.blue)

    def __eq__(self, other: ColorSpace):
        if isinstance(other, ColorSpace_RGB):
            return (
                self.red == other.red
                and self.green == other.green
                and self.blue == other.blue
                and self.alpha == other.alpha
            )
        return False

    def __neq__(self, other: ColorSpace):
        return not self.__eq__(other)

    def __mul__(self, other) -> ColorSpace_RGB:
        if isinstance(other, ColorSpace_RGB):
            return ColorSpace_RGB(
                red=self.red * other.red,
                green=self.green * other.green,
                blue=self.blue * other.blue,
                alpha=self.alpha * other.alpha,
            )
        else:
            raise TypeError(f"Cannot multiply {self} by {other}")

    def __truediv__(self, other) -> ColorSpace_RGB:
        if isinstance(other, ColorSpace_RGB):
            return ColorSpace_RGB(
                red=self.red / other.red,
                green=self.green / other.green,
                blue=self.blue / other.blue,
                alpha=self.alpha / other.alpha,
            )
        elif isinstance(other, (int, float)):
            return ColorSpace_RGB(
                red=(self.red / other),
                green=(self.green / other),
                blue=(self.green / other),
                alpha=self.alpha / other,
            )
        else:
            raise TypeError(f"Cannot divide {self} by {other}")

    def red_chromacity(self) -> ComponentValue:
        return self.red / (self.red + self.blue + self.green)

    def green_chromacity(self) -> ComponentValue:
        return self.green / (self.red + self.blue + self.green)

    @typing.override
    def to_rgb(self) -> ColorSpace_RGB:
        return self

    @typing.override
    @classmethod
    def from_rgb(cls: ColorSpace_RGB, model: ColorSpace_RGB) -> ColorSpace_RGB:
        return ColorSpace_RGB(model.red, model.green, model.blue, model.alpha)


###############################################################################
class ColorSpace_HSV(ColorSpace):
    """
    Hue, Saturation, and Value

    References
    ----------
    https://en.wikipedia.org/wiki/HSL_and_HSV
    """

    def __init__(
        self,
        hue: float | int | color_types.ComponentValue,
        saturation: float | int | color_types.ComponentValue,
        value: float | int | color_types.ComponentValue = 0.0,
    ) -> None:
        self.hue = color_types.ComponentValue(hue)
        self.saturation = color_types.ComponentValue(saturation)
        self.value = color_types.ComponentValue(value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.hue}, {self.saturation}, value={self.value})"

    def __copy__(self):
        return ColorSpace_HSV(self.hue, self.saturation, self.value)

    def to_rgb(self) -> ColorSpace_RGB:
        r, g, b = colorsys.hsv_to_rgb(
            float(self.hue), float(self.saturation), float(self.value)
        )
        return ColorSpace_RGB(r, g, b)


###############################################################################
class ColorSpace_HSL(ColorSpace):
    """
    Hue, Saturation, and Lightness

    References
    ----------
    https://en.wikipedia.org/wiki/HSL_and_HSV
    """

    def __init__(
        self,
        hue: float | int | color_types.ComponentValue,
        saturation: float | int | color_types.ComponentValue,
        lightness: float | int | color_types.ComponentValue = 0.0,
    ) -> None:
        self.hue = color_types.ComponentValue(hue)
        self.saturation = color_types.ComponentValue(saturation)
        self.lightness = color_types.ComponentValue(lightness)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.hue}, {self.saturation}, lightness={self.lightness})"

    def __copy__(self):
        return ColorSpace_HSL(self.hue, self.saturation, self.lightness)

    def to_rgb(self) -> ColorSpace_RGB:
        r, g, b = colorsys.hls_to_rgb(
            float(self.hue), float(self.saturation), float(self.lightness)
        )
        return ColorSpace_RGB(r, g, b)


###############################################################################
class ColorSpace_HSI(ColorSpace):
    """
    Hue, Saturation, and Light Intensity color space

    References
    ----------
    https://en.wikipedia.org/wiki/HSL_and_HSV
    """

    def __init__(
        self,
        hue: float | int | color_types.ComponentValue,
        saturation: float | int | color_types.ComponentValue,
        intensity: float | int | color_types.ComponentValue = 0.0,
    ) -> None:
        self.hue = color_types.ComponentValue(hue)
        self.saturation = color_types.ComponentValue(saturation)
        self.intensity = color_types.ComponentValue(intensity)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.hue}, {self.saturation}, intensity={self.intensity})"

    def __copy__(self):
        return ColorSpace_HSI(self.hue, self.saturation, self.intensity)

    def to_rgb(self) -> ColorSpace_RGB:
        r, g, b = colorsys.hls_to_rgb(
            float(self.hue), float(self.saturation), float(self.intensity)
        )
        return ColorSpace_RGB(r, g, b)


###############################################################################
class ColorSpace_TSL(ColorSpace):
    """
    Tint, Saturation, and Lightness

    References
    ----------
    https://en.wikipedia.org/wiki/TSL_color_space

    """

    def __init__(
        self,
        tint: float | int | color_types.ComponentValue = 0.0,
        saturation: float | int | color_types.ComponentValue = 0.0,
        lightness: float | int | color_types.ComponentValue = 0.0,
    ):
        self.tint = ComponentValue(tint)
        self.saturation = ComponentValue(saturation)
        self.lightness = ComponentValue(lightness)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tint={self.tint}, saturation={self.saturation}, lightness={self.lightness})"

    def __copy__(self):
        return ColorSpace_TSL(self.tint, self.saturation, self.lightness)

    @classmethod
    def from_rgb[T](cls: T, model: ColorSpace_RGB) -> T:
        """
        Transform an RGB color space into a TSL color space.

        Parameters
        ----------
        model

        Returns
        -------

        """
        tsl_model = ColorSpace_TSL()
        r_prime = model.red_chromacity() - (1 / 3)
        g_prime = model.green_chromacity() - (1 / 3)

        if g_prime != 0:
            tsl_model.tint = 0.5 - (math.atan2(g_prime, r_prime) / math.tau)
        else:
            tsl_model.tint = 0

        tsl_model.saturation = math.sqrt((9 / 5) * (r_prime**2 + g_prime**2))
        tsl_model.lightness = (
            (model.red * 0.299) + (model.green * 0.587) + (model.blue * 0.114)
        )

        return tsl_model

    def to_rgb(self) -> ColorSpace_RGB:
        """
        Transform into an RGB color space.

        Returns
        -------
        ColorSpace_RGB
            The RGB color space.

        """
        rgb_model = ColorSpace_RGB()
        x = math.tan(math.tau * (float(self.tint) - 0.25)) ** 2
        r_prime = math.sqrt((5 * float(self.saturation) ** 2) / (9 * ((x**-1) + 1)))
        g_prime = math.sqrt((5 * float(self.saturation) ** 2) / (9 * (x + 1)))
        r = r_prime + colorsys.ONE_THIRD
        g = g_prime + colorsys.ONE_THIRD
        k = self.lightness / (0.185 * r + 0.473 * g + 0.114)
        rgb_model.red = k * r
        rgb_model.green = k * g
        rgb_model.blue = k * (1 - r - g)

        return rgb_model


sp = ColorSpace_TSL.from_rgb(ColorSpace_RGB(255, 255, 255))
print(sp.to_rgb())
