# Examples

This directory contains small standalone Python scripts demonstrating
various capabilities of the ColorCode library.  Each file is executable when
run from the project root with `PYTHONPATH=.` so that the package can be
imported directly.

## Running an example

Activate your virtual environment (if you have one) and run e.g.: 

```bash
PYTHONPATH=. python3 examples/example_parse_color.py
```

The example scripts include an `Expected output` section at the top of each
file showing what you should see when the script runs successfully.

## Available examples

* `example_parse_color.py` – parsing helpers and `Color.create()`
* `example_models.py` – conversions between RGB and other color models
* `example_gradient.py` – generating color gradients and applying curves
* `example_manipulate_color.py` – color arithmetic, packing and chromacity

Feel free to open and adapt any script for your own explorations.
