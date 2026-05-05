from colorcode import Color, gradient, util, color_model
import pathlib


if __name__ == "__main__":
    start_color = Color(255, 0, 0)
    end_color = Color(0, 0, 254)

    curves = [
        (gradient.LinearCurve(), "linear"),
        (gradient.LogarithmicCurve(), "log"),
        (gradient.ExponentialCurve(), "exponential"),
        (gradient.RandomCurve(), "random"),
        (gradient.AgnesiWitchCurve(), "witch_of_agnesi"),
        (gradient.TriangleCurve(), "triangular"),
    ]

    for curve, name in curves:
        grad = gradient.Gradient(
            start_color,
            end_color,
            steps=100,
            model=color_model.RGB_Model(),
            curve=curve,
        )
        util.export_colorstrip(
            grad, pathlib.Path(__file__).parent.parent / f"assets/{name}_gradient.svg"
        )

    models = [
        (color_model.TSL_Model(), "tsl"),
        (color_model.RGB_Model(), "rgb"),
        (color_model.HSV_Model(), "hsv"),
        (color_model.YIQ_Model(), "yiq"),
        (color_model.YUV_Model(color_model.YUVStandard.BT709), "yuv"),
        (color_model.HSL_Model(), "hsl"),
    ]
    for model, name in models:
        grad = gradient.Gradient(
            start_color,
            end_color,
            steps=100,
            model=model,
            curve=gradient.LinearCurve(),
        )
        util.export_colorstrip(
            grad,
            pathlib.Path(__file__).parent.parent / f"assets/{name}_linear_gradient.svg",
        )
