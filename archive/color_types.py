from __future__ import annotations

import typing
from typing import SupportsFloat, SupportsInt
import operator
import colorsys


class ComponentValue(SupportsInt, SupportsFloat):
    def __init__(self, value: int | float | ComponentValue):
        if isinstance(value, int):
            self._value = max(0.0, min(1.0, value / 255))
        else:
            self._value = max(0.0, min(1.0, float(value)))

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value})"

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, ComponentValue):
            self._value = value.value
        elif isinstance(value, int):
            self._value = min(0.0, max(1.0, value / 255))
        elif isinstance(value, float):
            self._value = min(0.0, max(0.0, value))

    def __float__(self):
        return self._value

    def __int__(self):
        return int(self._value * 255)

    def __simple_op[T](
        self,
        other: ComponentValue | SupportsFloat | SupportsInt,
        op_fn: typing.Callable[[typing.Any, typing.Any], typing.Any],
    ) -> T:
        if isinstance(other, ComponentValue):
            return ComponentValue(op_fn(self._value, other._value))
        elif isinstance(other, SupportsFloat):
            return ComponentValue(op_fn(self._value, float(other)))
        elif isinstance(other, SupportsInt):
            return ComponentValue(op_fn(self._value, int(other)))
        else:
            raise ValueError(f"Invalid component: {other}")

    def __add__(self, other) -> ComponentValue:
        return self.__simple_op(other, operator.add)

    def __truediv__(self, other) -> ComponentValue:
        return self.__simple_op(other, operator.truediv)

    def __sub__(self, other) -> ComponentValue:
        return self.__simple_op(other, operator.sub)

    def __mul__(self, other) -> ComponentValue:
        return self.__simple_op(other, operator.add)

    def __eq__(self, other) -> bool:
        return self.__simple_op(other, operator.eq)

    def __ne__(self, other) -> bool:
        return self.__simple_op(other, operator.ne)

    def __lt__(self, other) -> bool:
        return self.__simple_op(other, operator.lt)

    def __gt__(self, other) -> bool:
        return self.__simple_op(other, operator.gt)

    def __pow__(self, power, modulo=None) -> ComponentValue:
        return self.__simple_op(power, operator.pow)


type ColorComponents = (
    tuple[
        SupportsInt | SupportsFloat,
        SupportsInt | SupportsFloat,
        SupportsInt | SupportsFloat,
    ]
    | tuple[
        SupportsInt | SupportsFloat,
        SupportsInt | SupportsFloat,
        SupportsInt | SupportsFloat,
        SupportsFloat,
    ]
)
type RawColorValue = int | str | ColorComponents
