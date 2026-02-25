"""
Gradient calulations between two colors.
"""

from .color import Color
from . import color_model
from .gradient_curve import GradientCurve, LinearCurve


###############################################################################
class Gradient(object):
    def __init__(
        self,
        start_color: Color,
        end_color: Color,
        model: color_model.ColorModel = color_model.RGB_Model(),
        curve: GradientCurve | None = None,
    ) -> None:
        """
        Calculates a gradient from the one color to another.

        Parameters
        ----------
        start_color : Color
            The start color of the gradient.
        end_color : Color
            The color at the end of the gradient.
        model : ColorModel
            The color model to use for calculating the gradient.
        curve : GradientCurve | None
            Callable that specifies how the color transitions from start to end.
        """
        self._start_color = start_color
        self._end_color = end_color
        self._model = model
        self._start_components = self._model.from_rgb(*start_color.rgb)
        self._end_components = self._model.from_rgb(*end_color.rgb)
        self._ranges = [c2 - c1 for c1, c2 in zip(self._start_components, self._end_components)]

        if curve is None:
            self._curve = LinearCurve()
        else:
            self._curve = curve

    def get_color(self, x: float) -> Color:
        """
        Get the value for x along the gradient, where 0 <= x <= 1
        The value x will be passed to the curve function if it
        has been set.

        Parameters
        ----------
        x : float
            The X-axis value along the gradient. This should be between 0 and 1

        Returns
        -------
        Color
            The color value for the given X-axis value along the gradient.

        """
        multiplier = self._curve(x)
        additions = [v * multiplier for v in self._ranges]
        new_values = []
        for n in range(len(self._start_components)):
            new_values.append(self._start_components[n] + additions[n])

        return Color(*self._model.to_rgb(*new_values))
