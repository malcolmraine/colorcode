from __future__ import annotations

import typing
from ._color_types import ComponentTuple


RGB_PREFIX: typing.Final[str] = "rgb"
RGBA_PREFIX: typing.Final[str] = "rgba"


def parse_color_string(
    color_string: str,
) -> ComponentTuple:
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
    cleaned_string = str(color_string).strip()
    if cleaned_string.startswith("#"):
        return parse_hex_string(cleaned_string)
    else:
        if cleaned_string.startswith(RGBA_PREFIX):
            cleaned_string = cleaned_string[len(RGBA_PREFIX) :]
        elif cleaned_string.startswith(RGB_PREFIX):
            cleaned_string = cleaned_string[len(RGB_PREFIX) :]
        string_parts = cleaned_string.strip("(").strip(")").split(",")
        return tuple(map(int, string_parts))


def parse_hex_string(
    hex_string: str,
) -> ComponentTuple:
    """
    Parse a hex string into a tuple.

    Parameters
    ----------
    hex_string : str
    The raw string describing the color. Should be in the format #FFFFFFFF or #FFFFFF

    Returns
    -------
    tuple[int, ...]
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
            int(cleaned_string[6:8], 16),
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


def parse_color_int(color_int: int) -> ComponentTuple:
    """
    Convert an integer into color components.

    Parameters
    ----------
    color_int : int
        The raw integer describing the color.

    Returns
    -------
    ColorComponents
        A tuple of color components.

    """
    alpha: int | None = None

    if (color_int + 1) >= 2**32:
        # There are 4 components
        alpha = color_int >> 24
    green = color_int >> 16
    blue = color_int >> 8
    red = color_int & 0xFF

    if alpha is not None:
        return red, green, blue, alpha
    return red, green, blue
