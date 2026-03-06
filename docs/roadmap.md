
# Development Roadmap

## Utilities

### Color picker dialog

Simple Tkinter dialog that allows for changing between color spaces and controlling the levels of each component

- Should Show a sample rectangle of the chosen color.
- There should be sliders for each component of the color model.
- Switching between color models should not change the chosen color.
- Users should be able to see the different color code formats for the current color.
- 

### Exporting colorstrips

- [ ] SVG


## Color model support

- Cylindrical color models
  - [ ] HWB (Hue, Whiteness, Blackness)
    - https://en.wikipedia.org/wiki/HWB_color_model
  - [ ] HCT 
  - [ ] HCL
    - https://en.wikipedia.org/wiki/HCL_color_space
  - [ ] CIELCH / LCH 
  - [ ] CIECAM02 
    - https://en.wikipedia.org/wiki/CIECAM02
- Subtractive color models
  - [ ] CMY, CMYK
    - https://en.wikipedia.org/wiki/CMYK_color_model
  - [ ] RYB
    - https://en.wikipedia.org/wiki/RYB_color_model
- Other
  - [ ] YUV
    - https://en.wikipedia.org/wiki/Y′UV
  - [ ] YCoCg
    - https://en.wikipedia.org/wiki/YCoCg

## Alpha compositing

## Color manipulation

- [ ] Arithmetic on Color instances
- [ ] Comparison operators for Color instances
- [ ] Color inversion
  - Should be able to specify the color model used for inversion.
- [ ] Contrast ratio calculation and optimization


## Gradients

# Gradient curves

- [ ] Sigmoid
- [x] Triangle
- [ ] Random
- [ ] Bezier
- [ ] Trapezoid
  - Vertices should be parameterizable