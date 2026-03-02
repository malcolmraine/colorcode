![ColorCode](./assets/colorcode_logo_with_name.svg)

![Tests](https://github.com/malcolmraine/colorcode/actions/workflows/tests.yml/badge.svg)
![Ruff](https://github.com/malcolmraine/colorcode/actions/workflows/ruff.yml/badge.svg)
![Mypy](https://github.com/malcolmraine/colorcode/actions/workflows/mypy.yml/badge.svg)


## ColorCode — Python library for handling colors

ColorCode provides utilities and classes for parsing, converting and
manipulating colors across multiple color spaces. It is lightweight and
designed for programmatic color work and small scripts.

Highlights
----------

- Parsing helpers for hex strings, `rgb(...)`/`rgba(...)` strings and packed
  integers
- A `Color` class exposing `rgb`, `rgba`, `hsv`, `hls`, `tsl` and `yiq`
  properties
- Several `ColorModel` implementations: `RGB`, `HSV`, `HSL`, `YIQ` and `TSL`
- Gradient generation with configurable curves (linear, exponential,
  logarithmic)


Quick usage
-----------

Create a `Color` and convert between representations:

```python
from colorcode import color

c = color.Color(255, 128, 0)  # orange
print(c.rgb)   # (255, 128, 0)
print(c.hsv)   # hue, saturation, value
c.hsv = (180, 1, 1)           # set color via HSV
```

Use models directly:

```python
from colorcode import color_model

model = color_model.HSV_Model()
rgb = (0.1, 0.2, 0.3)
h, s, v = model.from_rgb(*rgb)
rgb_back = model.to_rgb(h, s, v)
```

Generate a gradient:

```python
from colorcode import color, gradient

start = color.Color(0, 0, 0)
end = color.Color(255, 255, 255)
g = gradient.Gradient(start, end, steps=5)
for step in g:
    print(step.rgb)
```

Tests and docs
--------------

Run the test suite with:

```bash
python3 -m unittest discover -v
```

See `docs/color_models.md` for model explanations and `docs/gradients.md` for
gradient usage and curve documentation.
