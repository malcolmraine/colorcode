import colorsys
import math
from abc import abstractmethod, ABC
import enum


def calc_red_chromacity(red: float, green: float, blue: float) -> float:
    return red / (red + blue + green)


def calc_green_chromacity(red: float, green: float, blue: float) -> float:
    return green / (red + blue + green)


###############################################################################
class ColorComponent(enum.StrEnum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    HUE = "Hue"
    SATURATION = "Saturation"
    VALUE = "Value"
    LIGHTNESS = "Lightness"
    TINT = "Tint"


###############################################################################
class ColorModel(ABC):
    @abstractmethod
    def to_rgb(self, *args: float) -> tuple[float, float, float]: ...

    @abstractmethod
    def from_rgb(self, red: float, green: float, blue: float) -> tuple[float, ...]: ...


###############################################################################
class RGB_Model(ColorModel):
    """
    Pass through color model.
    """

    def to_rgb(
        self, red: float, green: float, blue: float
    ) -> tuple[float, float, float]:
        return red, green, blue

    def from_rgb(
        self, red: float, green: float, blue: float
    ) -> tuple[float, float, float]:
        return red, green, blue


###############################################################################
class TSL_Model(ColorModel):
    def to_rgb(
        self, tint: float, saturation: float, lightness: float
    ) -> tuple[float, float, float]:
        x = math.tan(math.tau * (float(tint) - 0.25)) ** 2
        r_prime = math.sqrt((5 * float(saturation) ** 2) / (9 * ((x**-1) + 1)))
        g_prime = math.sqrt((5 * float(saturation) ** 2) / (9 * (x + 1)))
        r = r_prime + colorsys.ONE_THIRD
        g = g_prime + colorsys.ONE_THIRD
        k = lightness / (0.185 * r + 0.473 * g + 0.114)
        red = k * r
        green = k * g
        blue = k * (1 - r - g)

        return red, green, blue

    def from_rgb(
        self, red: float, green: float, blue: float
    ) -> tuple[float, float, float]:
        r_prime = calc_red_chromacity(red, green, blue) - colorsys.ONE_THIRD
        g_prime = calc_green_chromacity(red, green, blue) - colorsys.ONE_THIRD

        if g_prime != 0:
            tint = 0.5 - (math.atan2(g_prime, r_prime) / math.tau)
        else:
            tint = 0

        saturation = math.sqrt((9 / 5) * (r_prime**2 + g_prime**2))
        lightness = (red * 0.299) + (green * 0.587) + (blue * 0.114)
        return tint, saturation, lightness


###############################################################################
class HSV_Model(ColorModel):
    def to_rgb(
        self, hue: float, saturation: float, value: float
    ) -> tuple[float, float, float]:
        return colorsys.hsv_to_rgb(hue, saturation, value)

    def from_rgb(
        self, red: float, green: float, blue: float
    ) -> tuple[float, float, float]:
        return colorsys.rgb_to_hsv(red, green, blue)


###############################################################################
class HSL_Model(ColorModel):
    def to_rgb(
        self, hue: float, saturation: float, lightness: float
    ) -> tuple[float, float, float]:
        return colorsys.hls_to_rgb(hue, saturation, lightness)

    def from_rgb(
        self, red: float, green: float, blue: float
    ) -> tuple[float, float, float]:
        h, l, s = colorsys.rgb_to_hls(red, green, blue)
        return h, s, l


###############################################################################
class YIQ_Model(ColorModel):
    def to_rgb(self, y: float, i: float, q: float) -> tuple[float, float, float]:
        return colorsys.yiq_to_rgb(y, i, q)

    def from_rgb(
        self, red: float, green: float, blue: float
    ) -> tuple[float, float, float]:
        return colorsys.yiq_to_rgb(red, green, blue)
