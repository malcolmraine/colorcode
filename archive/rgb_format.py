from __future__ import annotations

import enum


class RGBFormat(enum.StrEnum):
    RGB = "RGB"
    RGBA = "RGBA"
    BGR = "BGR"
    BGRA = "BGRA"

    def has_alpha(self) -> bool:
        return self in (RGBFormat.RGBA, RGBFormat.BGRA)

    @classmethod
    def create(cls, value: str) -> RGBFormat:
        return RGBFormat(str(value).upper())
