##
from __future__ import annotations

import enum
import typing


class ColorFormat(enum.StrEnum):
    RGB = "RGB"
    RGBA = "RGBA"
    BGR = "BGR"
    BGRA = "BGRA"

    def has_alpha(self) -> bool:
        return self in (ColorFormat.RGBA, ColorFormat.BGRA)

    @classmethod
    def create(cls, value: str) -> ColorFormat:
        return ColorFormat(str(value).upper())


ColorComponents: typing.TypeAlias = tuple[int, int, int] | tuple[int, int, int, float]
RawColorValue: typing.TypeAlias = int | str | ColorComponents


class Color(object):
    def __init__(
        self,
        red: int | float = 0,
        green: int | float = 0,
        blue: int | float = 0,
        alpha: int | float = 1.0,
        color_format: ColorFormat = ColorFormat.RGB,
    ) -> None:
        """
        Parameters
        ----------
        red : int | float
            Red component of the color.
        green : int | float
            Green component of the color.
        blue : int | float
            Blue component of the color.
        alpha : int | float
            Alpha component of the color.
        color_format : ColorFormat
            The format of the color components.
        """
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        self.color_format: ColorFormat = color_format

        if isinstance(red, float):
            self.red = int(255 * red)

        if isinstance(green, float):
            self.green = int(255 * green)

        if isinstance(blue, float):
            self.blue = int(255 * blue)

        if isinstance(alpha, int) and self.color_format.has_alpha():
            self.alpha = float(max(min(0, alpha), 1.0) / 255)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(r={self.red}, g={self.green}, b={self.blue}, a={self.alpha})"

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.as_tuple()[item]
        raise IndexError(f"Index out of range: {item}")

    def __mul__(self, other) -> Color:
        if isinstance(other, Color):
            return Color(
                red=self.red * other.red,
                green=self.green * other.green,
                alpha=self.alpha * other.alpha,
                color_format=self.color_format,
            )
        elif isinstance(other, ColorComponents):
            return self + Color.from_tuple(other)
        else:
            raise TypeError(f"Cannot multiply {self} by {other}")

    def __truediv__(self, other) -> Color:
        if isinstance(other, Color):
            return Color(
                red=self.red / other.red,
                green=self.green / other.green,
                alpha=self.alpha / other.alpha,
                color_format=self.color_format,
            )
        elif isinstance(other, tuple):
            return self + Color.from_tuple(other)
        elif isinstance(other, (int, float)):
            return Color(
                red=int(self.red / other),
                green=int(self.green / other),
                alpha=self.alpha / other,
                color_format=self.color_format,
            )
        else:
            raise TypeError(f"Cannot divide {self} by {other}")

    def __add__(self, other) -> Color:
        if isinstance(other, Color):
            return Color(
                red=self.red + other.red,
                green=self.green + other.green,
                alpha=self.alpha + other.alpha,
                color_format=self.color_format,
            )
        elif isinstance(other, ColorComponents):
            return self + Color.from_tuple(other)
        else:
            raise TypeError(f"Cannot add {other} to {self}")

    def __sub__(self, other):
        if isinstance(other, Color):
            return Color(
                red=self.red - other.red,
                green=self.green - other.green,
                alpha=self.alpha - other.alpha,
                color_format=self.color_format,
            )
        elif isinstance(other, ColorComponents):
            return self - Color.from_tuple(other)
        else:
            raise TypeError(f"Cannot subtract {other} from {self}")

    @classmethod
    def parse_color_string(cls, color_string: str) -> ColorComponents:
        """

        Parameters
        ----------
        color_string : str
            The raw string describing the color.

        Returns
        -------
        ColorComponents
            A tuple of color components.

        Raises
        ------
        ValueError
            Raised if the color string is invalid.

        """
        cleaned_string = color_string.strip()
        if cleaned_string.startswith("#"):
            return cls.parse_hex_string(cleaned_string)
        else:
            if cleaned_string.startswith("rgb"):
                cleaned_string.strip("rgb")
            elif cleaned_string.startswith("rgba"):
                cleaned_string.strip("rgba")
            string_parts = cleaned_string.strip("(").strip(")").split(",")
            return tuple(map(int, string_parts))

    @staticmethod
    def parse_hex_string(hex_string: str) -> ColorComponents:
        """
        Parse a hex string into a ColorComponent tuple.

        Parameters
        ----------
        hex_string : str
        The raw string describing the color. Should be in the format #FFFFFFFF or #FFFFFF

        Returns
        -------
        ColorComponents
            A tuple of color components.

        Raises
        ------
        ValueError
            Raised if the hex string is invalid.
        """
        cleaned_string = hex_string.strip().strip("#")
        if len(cleaned_string) == 8:
            components = (
                int(cleaned_string[0:2], 16),
                int(cleaned_string[2:4], 16),
                int(cleaned_string[4:6], 16),
                round(int(cleaned_string[6:8], 16) / 255, 3),
            )
        elif len(cleaned_string) == 6:
            components = (
                int(cleaned_string[0:2], 16),
                int(cleaned_string[2:4], 16),
                int(cleaned_string[4:6], 16),
            )
        else:
            raise ValueError(f"Invalid hex string: {hex_string}")

        return components

    @classmethod
    def from_hex(
        cls, hex_string: str, color_format: ColorFormat | None = None
    ) -> Color:
        """

        Parameters
        ----------
        hex_string : str
            The raw hex string describing the color.

        color_format : ColorFormat | None
            The format of the color components. If None is given, the format is
            assumed to be RGB or RGBA, depending on the length of the string.

        Returns
        -------
        Color
            The color instance.
        """
        if color_format is None:
            given_format = ColorFormat.RGB
        else:
            given_format = color_format

        components = cls.parse_hex_string(hex_string)
        if color_format is None and len(components) == 4:
            given_format = ColorFormat.RGBA

        return cls.from_tuple(components, given_format)

    @staticmethod
    def parse_color_int(
        color_int: int, color_format: ColorFormat | None = None
    ) -> ColorComponents:
        """
        Convert an integer into color components.

        Parameters
        ----------
        color_int : int
            The raw integer describing the color.
        color_format : ColorFormat | None
            The format of the color components. If None is given, the format is assumed to be RGB.

        Returns
        -------
        ColorComponents
            A tuple of color components.

        """
        components = []
        if color_format is not None and color_format.has_alpha():
            components.append(color_int >> 24)
        components.append(color_int >> 16)
        components.append(color_int >> 8)
        components.append(color_int & 0xFF)

        return (*components,)

    @staticmethod
    def reorder_color_components(
        color_components: ColorComponents,
        from_format: ColorFormat,
        to_format: ColorFormat,
    ) -> ColorComponents:
        """
        Change the order of the color components from one format to another.

        Parameters
        ----------
        color_components : ColorComponents
            The color components to reorder.
        from_format : ColorFormat
            The format of the input color components.
        to_format : ColorFormat
            The format of the output color components.

        Returns
        -------
        ColorComponents
            The reordered color components.

        Raises
        ------
        ValueError
            Raised if the color components are invalid.
        """
        r, g, b, a = 0, 0, 0, 1.0

        match from_format:
            case ColorFormat.RGB:
                r, g, b = color_components
            case ColorFormat.RGBA:
                r, g, b, a = color_components
            case ColorFormat.BGR:
                b, g, r = color_components
            case ColorFormat.BGRA:
                b, g, r, a = color_components
            case _:
                raise ValueError(f"Unknown color format: {from_format}")

        match to_format:
            case ColorFormat.RGB:
                return r, g, b
            case ColorFormat.RGBA:
                return r, g, b, a
            case ColorFormat.BGR:
                return b, g, r
            case ColorFormat.BGRA:
                return b, g, r, a
            case _:
                raise ValueError(f"Unknown color format: {to_format}")

    @classmethod
    def create(
        cls, color: Color | RawColorValue, color_format: ColorFormat | None = None
    ) -> Color | None:
        if isinstance(color, Color):
            return color
        if isinstance(color, str):
            return cls.from_tuple(cls.parse_color_string(color), color_format)
        if isinstance(color, tuple):
            return cls.from_tuple(color, color_format)
        if isinstance(color, int):
            return cls.from_tuple(
                cls.parse_color_int(color, color_format), color_format
            )
        return None

    @classmethod
    def from_tuple(
        cls,
        color_components: ColorComponents,
        color_format: ColorFormat | None = None,
    ) -> Color:
        """
        Create a Color instance from a tuple of color components.

        Parameters
        ----------
        color_components : ColorComponents
            The color components to use to create the Color instance.
        color_format : ColorFormat
            The format of the color components. If None is given, the format is assumed to be RGB.

        Returns
        -------
        Color

        Raises
        ------
        ValueError
            Raised if the color components are invalid.
        """
        if color_format is None:
            if len(color_components) == 4:
                given_format = ColorFormat.RGBA
            else:
                given_format = ColorFormat.RGB

        if len(color_components) == 3:
            r, g, b = cls.reorder_color_components(
                color_components, given_format, ColorFormat.RGB
            )
            return cls(red=r, green=g, blue=b, color_format=given_format)
        elif len(color_components) == 4:
            r, g, b, a = cls.reorder_color_components(
                color_components, given_format, ColorFormat.RGBA
            )
            return cls(
                red=r, green=g, blue=b, alpha=float(a), color_format=given_format
            )
        else:
            raise ValueError(f"Invalid color format: {color_components}")

    def to_tuple(self) -> ColorComponents:
        """
        Get the colors components as a tuple.

        Returns
        -------
        tuple[int, int, int, float] | tuple[int, int, int, float]
            Returns a tuple of r, g, b or r, g, b, a depending on the color format.
        """
        match self.color_format:
            case ColorFormat.RGB:
                return self.red, self.green, self.blue
            case ColorFormat.RGBA:
                return self.red, self.green, self.blue, self.alpha
            case ColorFormat.BGR:
                return self.blue, self.green, self.blue
            case ColorFormat.BGRA:
                return self.blue, self.green, self.red, self.alpha
            case _:
                raise ValueError(f"Unknown color format: {self.color_format}")

    def to_hex(self, formatted: bool = True):
        """

        Parameters
        ----------
        formatted : bool
            If True, prefix the hex string with a '#'

        Returns
        -------
        hex : str
            The hexadecimal representation of the color as a string.
        """
        hex_string = ""
        if formatted:
            hex_string += "#"

        components = self.to_tuple()
        for component in components:
            hex_string += f"{component:02x}"

        return hex_string

    def set_opacity(
        self, opacity: float, background_color: Color | RawColorValue
    ) -> None:
        bg_color = self.create(background_color)
        if self.color_format.has_alpha():
            self.alpha = opacity
        else:
            # Use alpha compositing to simulate the transparency
            ...


#
# cl = Color(255, 0, 0, 0.0)
#
# print(cl)
# print(cl.as_hex())

print(Color.create("#ffffff7f") / 2)
# print(hex((255 << 16) + (255 << 8) + (255)))
