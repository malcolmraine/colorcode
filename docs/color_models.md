# Color Models

ColorCode supports conversions between various color models. Below are the
models implemented in this library along with short explanations and code
snippets showing how to use the `ColorModel` classes.

| Model | Description                                    |
|:-----:|:-----------------------------------------------|
|  RGB  | Red, Green, Blue (pass-through)                |
|  HSV  | Hue, Saturation, Value                         |
|  HSL  | Hue, Saturation, Lightness                     |
|  YIQ  | Luma / chrominance (NTSC)                      |
|  TSL  | Tint, Saturation, Lightness (library-specific) |



## Creating models via factory method

Use `colormodel.create` with a `ColorModelType` to obtain a model instance:

```python
from colorcode import color_model

m = color_model.create(color_model.ColorModelType.HSV)
```


## Using the `Color` API

`color.Color` instances expose properties that delegate to these models. For
example, `c.hsv`, `c.hls`, `c.tsl`, and `c.yiq` provide easy conversion access
from a `Color` object:

```python
from colorcode import color

c = color.Color(255, 0, 0)   # red
print(c.hsv)                # (hue, saturation, value)
c.hsv = (120, 1, 1)         # set to green via HSV
```

These snippets should help you get started exploring different color
representations in the library.

## RGB

RGB contains explicit red, green and blue channels. The `RGB_Model` in
ColorCode simply passes values through and is useful when you want to work
directly with RGB components.

#### Example

```python
from colorcode.color_model import RGB_Model

model = RGB_Model()
rgb = (0.2, 0.4, 0.6)
print(model.to_rgb(*rgb))     # (0.2, 0.4, 0.6)
print(model.from_rgb(*rgb))   # (0.2, 0.4, 0.6)
```

## HSV

HSV represents colors as Hue, Saturation and Value. ColorCode's `HSV_Model`
uses Python's `colorsys` conversions under the hood.

#### Example

```python
from colorcode.color_model import HSV_Model

model = HSV_Model()
rgb = (0.1, 0.2, 0.3)
h, s, v = model.from_rgb(*rgb)
rgb_back = model.to_rgb(h, s, v)
```

## HSL

HSL uses Hue, Saturation and Lightness. Note that `colorsys` exposes HLS
ordering; the library's `HSL_Model` adjusts argument order so callers can use
the more common HSL parameter ordering.

#### Example

```python
from colorcode.color_model import HSL_Model

model = HSL_Model()
rgb = (0.2, 0.4, 0.6)
h, s, l = model.from_rgb(*rgb)
rgb_back = model.to_rgb(h, s, l)
```

## YIQ

YIQ is a luma/chrominance model historically used for NTSC television. The
`YIQ_Model` wraps `colorsys.yiq_to_rgb` and `colorsys.rgb_to_yiq` conversions.

#### Example

```python
from colorcode.color_model import YIQ_Model

model = YIQ_Model()
rgb = (0.5, 0.4, 0.3)
y, i, q = model.from_rgb(*rgb)
rgb_back = model.to_rgb(y, i, q)
```

## TSL

TSL is a model used within this library representing Tint, Saturation and
Lightness. Implementations are approximate; conversions may not perfectly
invert due to the chosen transforms, so prefer TSL for perceptual operations
rather than byte-perfect round-trips.

#### Example

```python
from colorcode.color_model import TSL_Model

model = TSL_Model()
rgb = (0.3, 0.6, 0.9)
t, s, l = model.from_rgb(*rgb)
rgb_back = model.to_rgb(t, s, l)
```



