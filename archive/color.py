from color_space import (
    ColorSpace,
    ColorSpace_RGB,
    ColorSpace_HSV,
    ColorSpace_TSL,
    ColorSpace_HSI,
    ColorSpace_HSL,
)
from color_types import ComponentValue, ColorComponents
from colorcode.color_types import RawColorValue


class Color(object):
    def __init__(
        self,
        red: ComponentValue | int | float | None = 0.0,
        green: ComponentValue | int | float | None = 0.0,
        blue: ComponentValue | int | float | None = 0.0,
        model: ColorSpace | None = None,
    ) -> None:
        if model is None:
            self.colorspace = ColorSpace_RGB(red, green, blue)
        else:
            self.colorspace = model
            if hasattr(self.colorspace, "opacity"):
                self.opacity = self.colorspace.opacity

    @property
    def red(self) -> ComponentValue:
        if isinstance(self.colorspace, ColorSpace_RGB):
            return self.colorspace.red
        else:
            return self.colorspace.to_rgb().red

    @red.setter
    def red(self, value: ComponentValue) -> None: ...

    @property
    def green(self) -> ComponentValue:
        if isinstance(self.colorspace, ColorSpace_RGB):
            return self.colorspace.green
        else:
            return self.colorspace.to_rgb().green

    @green.setter
    def green(self, value: ComponentValue) -> None: ...

    @property
    def blue(self) -> ComponentValue:
        if isinstance(self.colorspace, ColorSpace_RGB):
            return self.colorspace.green
        else:
            return self.colorspace.to_rgb().blue

    @blue.setter
    def blue(self, value: ComponentValue) -> None:
        if isinstance(self.colorspace, ColorSpace_RGB):
            self.colorspace.blue = value
        else:
            # TODO: Do conversion back and forth to modify colorspace.
            ...

    @property
    def opacity(self) -> ComponentValue:
        if isinstance(self.colorspace, ColorSpace_RGB):
            return self.colorspace.alpha
        else:
            return self.colorspace.to_rgb().alpha

    @property
    def lightness(self) -> ComponentValue:
        if isinstance(self.colorspace, (ColorSpace_TSL, ColorSpace_HSL)):
            return self.colorspace.lightness

    @lightness.setter
    def lightness(self, value: ComponentValue) -> None:
        if isinstance(self.colorspace, ColorSpace_TSL, ColorSpace_HSL):
            self.colorspace.lightness = value

    @property
    def saturation(self) -> ComponentValue: ...

    @saturation.setter
    def saturation(self, value: ColorComponents) -> None:
        if isinstance(
            self.colorspace,
            (ColorSpace_TSL, ColorSpace_HSI, ColorSpace_HSL, ColorSpace_HSV),
        ):
            self.colorspace.saturation = value

    @property
    def tint(self) -> ComponentValue: ...

    @tint.setter
    def tint(self, value: ComponentValue) -> None:
        if isinstance(self.colorspace, ColorSpace_TSL):
            self.colorspace.tint = value
