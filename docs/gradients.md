# Gradients
Gradients between two colors can be defined according to various pre-defined or user defined curves


``` python
from colorcode import Color, Gradient

start_color = Color.create("#FFCB6B")
end_color = Color.create("#3D8BFF")
gradient = Gradient(start_color, end_color)

colors = []
for i in range(0, 50):
    colors.append(gradient.get_color(i / 100))

```
![Linear Gradient Example](../assets/linear_gradient.svg)

## Gradient Curves
How the gradient transitions from the start color to the end color can be controlled by selecting different gradient curves.
There are a few different curves defined in this library but users can create their own custom GradientCurve subclasses.
The predefined gradient curves are described below. All the examples start at `rgb(255, 203, 0)` and end at `rgb(30, 75, 254)`.

### Linear Curve
$f(x) = x\ \ \{0 \le x \le 1\}$

![Linear Gradient Example](../assets/linear_gradient.svg)

### Logarithmic Curve
$f(x) = k * log (x) + 1\ \ \{0 \le x \le 1\}$

Default is $k=0.5$

![Logarithmic Gradient Example](../assets/log_gradient.svg)

### Exponential Curve
$f(x) = x^n\ \ \{0 \le x \le 1\}$

Default is $n=2$

![Exponential Gradient Example](../assets/exponential_gradient.svg)

### Witch of Agnesi Curve
This is a modified version of the Witch of Agnesi curve.
See https://en.wikipedia.org/wiki/Witch_of_Agnesi


$f(x) = \frac{8a^{2.2154}}{(x-0.5)^2+(4a^2)} \ \{0 \le x \le 1\}$

Default is $a=0.04$


![Witch of Agnesi Gradient Example](../assets/witch_of_agnesi_gradient.svg)


### Triangular Curve

$
f(x) = \begin{cases}
2x& \text{if } 0 \leq x \leq 0.5,\\
(1 - (0.5x)) - 1  & 0.5 \lt x \leq 1 \\
\end{cases}
$

![Triangular Gradient Example](../assets/triangular_gradient.svg)