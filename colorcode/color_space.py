from __future__ import annotations
import abc
import math


class ColorSpace(object, abc.ABC):
    @classmethod
    def from_rgb[T](cls: T, model: ColorSpace_RGB) -> T: ...

    @abc.abstractmethod
    def to_rgb(self) -> ColorSpace_RGB: ...


class ColorSpace_RGB(ColorSpace):
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def red_chromacity(self):
        return self.red / (self.red + self.blue + self.green)

    def green_chromacity(self):
        return self.green / (self.red + self.blue + self.green)


class ColorSpace_HSV(ColorSpace): ...


class ColorSpace_HSL(ColorSpace): ...


class ColorSpace_HSI(ColorSpace): ...


class ColorSpace_TSL(ColorSpace):
    """
    https://en.wikipedia.org/wiki/TSL_color_space

    """

    def __init__(
        self, tint: float = 0.0, saturation: float = 0.0, luminosity: float = 0.0
    ):
        self.tint = 0
        self.saturation = 0
        self.luminosity = 0

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
        tsl_model.luminosity = (
            0.299 * model.red + 0.587 * model.green + 0.114 * model.blue
        )

        return tsl_model

    def to_rgb(self) -> ColorSpace_RGB:
        """
        Transform into an RGB color space.

        Returns
        -------

        """
        rgb_model = ColorSpace_RGB()
        x = math.tan2(math.tau * (self.tint - 0.25))
        r_prime = math.sqrt((5 * self.saturation**2) / (9 * ((x**-1) + 1)))
        g_prime = math.sqrt((5 * self.saturation**2) / (9 * (x + 1)))
        r = r_prime + (1 / 3)
        g = g_prime + (1 / 3)
        k = self.luminosity / (0.185 * r + 0.473 * g + 0.114)
        rgb_model.red = k * r
        rgb_model.green = k * g
        rgb_model.blue = k * (1 - r - g)

        return rgb_model
