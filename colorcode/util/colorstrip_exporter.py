"""
File: colorcode/util/colorstrip_exporter.py
Description: Exports colors to an SVG color strip.
Author: Malcolm Hall
License: MIT
"""

from __future__ import annotations

from string import Template
import pathlib
import os
from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from colorcode.color import Color


svg_template = Template("""<?xml version="1.0" encoding="iso-8859-1"?>

<svg version="1.1" id="Layer_1" 
     xmlns="http://www.w3.org/2000/svg" 
     x="0px" y="0px"
	 viewBox="0 0 $WIDTH $HEIGHT" 
     style="enable-background:new 0 0 $WIDTH $HEIGHT;"
     xml:space="preserve"
     $CRISP_SHAPE_RENDERING
     >
$SLICE_FILL
</svg>
""")

slice_template = Template(
    '<rect x="$X_POS" y="0" style="fill:rgba($RED, $GREEN, $BLUE, $ALPHA);" width="$SLICE_WIDTH" height="$HEIGHT"/>'
)


class ColorStripExporter(ABC):
    @abstractmethod
    def save(self, filename: pathlib.Path | str) -> None: ...


class SvgExporter(ColorStripExporter):
    def __init__(
        self, color_list: list[Color], image_width: int = 512, image_height: int = 128
    ) -> None:
        self.color_list = color_list
        self.image_width = image_width
        self.image_height = image_height
        self.crisp_shape_rendering = True

        if not color_list:
            self._slice_width = 0
        else:
            self._slice_width = int(self.image_width / len(self.color_list))

    def is_valid(self) -> bool:
        if (
            len(self.color_list) == 0
            or self._slice_width <= 0
            or self.image_height <= 0
            or self.image_width <= 0
        ):
            return False
        return True

    def save(self, filename: pathlib.Path | str) -> None:
        slice_xml = ""
        x_pos = 0

        for color in self.color_list:
            r, g, b, a = color.rgba
            slice_xml += (
                "    "
                + slice_template.substitute(
                    {
                        "SLICE_WIDTH": str(self._slice_width),
                        "HEIGHT": str(self.image_height),
                        "RED": str(round(r)),
                        "GREEN": str(round(g)),
                        "BLUE": str((round(b))),
                        "ALPHA": str(round(a / color.base)),
                        "X_POS": str(x_pos),
                    }
                )
                + "\n"
            )
            x_pos += self._slice_width

        svg_dict = {
            "WIDTH": str(self.image_width),
            "HEIGHT": str(self.image_height),
            "SLICE_FILL": slice_xml,
        }

        if self.crisp_shape_rendering:
            svg_dict["CRISP_SHAPE_RENDERING"] = 'shape-rendering="crispEdges"'
        else:
            svg_dict["CRISP_SHAPE_RENDERING"] = ""
        svg_xml = svg_template.substitute(svg_dict)

        file_dir = os.path.dirname(filename)
        os.makedirs(file_dir, exist_ok=True)

        with open(str(filename), "w") as f:
            f.write(svg_xml)


def export_colorstrip(
    color_list: typing.Iterable[Color],
    filename: pathlib.Path | str,
    image_width: int = 512,
    image_height: int = 128,
) -> None:
    exporter = SvgExporter(
        list(color_list), image_width=image_width, image_height=image_height
    )
    exporter.save(filename)
