# pyctorial

```
pip install pyctorial
```

**pyctorial** is a Python library for **generating patterns and manipulating images**. It provides tools for:

* Generative gradients
* Halftone rendering (bitmap and vector)
* Image slicing
* Gradient stretching
* Programmatic image pipelines

It is designed to work both:

* **Inside Python scripts**
* **Directly from the command line**

The library focuses on a **simple functional API** where most operations:

* take a `PIL.Image`
* return a new `PIL.Image`

This makes it easy to **compose multiple operations together**.

---

# Installation

```
pip install pyctorial
```

For development:

```
git clone https://github.com/decentishdev/pyctorial
cd pyctorial
pip install -e .
```

---

# Quick Example

```python
import pyctorial as px

img = px.load("photo.jpg")

dots = px.halftone(img)

px.save(dots, "halftone.png")
```

---

# Command Line Example

```
pyctorial halftone photo.jpg dots.png
```

---

# Philosophy

Most functions follow a simple pattern:

```
Image -> transform -> Image
```

This allows **composable pipelines**:

```python
import pyctorial as px

img = px.load("portrait.jpg")

img = px.halftone(img)
img = px.gradient_stretch(img, x_start=400)

px.save(img, "result.png")
```

---

# Core API

## Image IO

These functions allow loading and saving images.

### Load Image

```python
import pyctorial as px

img = px.load("input.png")
```

Optional mode conversion:

```python
img = px.load("photo.jpg", mode="L")
```

### Save Image

```python
px.save(img, "output.png")
```

---

# Filters

Filters modify an existing image.

---

# Halftone Filter

Creates a **dot halftone effect** similar to old print media.

## Python Usage

```python
import pyctorial as px

img = px.load("portrait.jpg")

dots = px.halftone(
    img,
    cell_size=12,
    max_dot_ratio=0.9
)

px.save(dots, "dots.png")
```

### Parameters

| Parameter       | Description                       |
| --------------- | --------------------------------- |
| `cell_size`     | Size of the halftone grid         |
| `max_dot_ratio` | Maximum dot size relative to cell |
| `invert`        | Invert brightness mapping         |

### Example

```python
dots = px.halftone(img, cell_size=8)
```

---

# Vector Halftone (SVG)

Generates a **vector halftone** that scales infinitely.

Returns an SVG string.

## Python Example

```python
svg = px.halftone_svg(img)

px.save_svg(svg)
```

### Example with parameters

```python
svg = px.halftone_svg(
    img,
    cell_size=10,
    max_dot_ratio=0.8
)
```

---

# Pattern Generation

Pattern generators **create new images from scratch**.

---

# Noisy Gradient

Creates a **blurred, warped, generative gradient**.

This gradient uses:

* focal color points
* gaussian blur
* Perlin noise warping
* film grain

## Python Example

```python
import pyctorial as px

img = px.noisy_gradient(
    width=1200,
    height=800,
    num_focal_points=6
)

px.save(img, "gradient.png")
```

### Parameters

| Parameter          | Description                  |
| ------------------ | ---------------------------- |
| `width`            | Output width                 |
| `height`           | Output height                |
| `num_focal_points` | Number of color sources      |
| `blur_strength`    | Amount of gradient blur      |
| `warp_strength`    | Strength of noise distortion |

### Example

```python
img = px.noisy_gradient(
    2000,
    2000,
    num_focal_points=10,
    blur_strength=300
)
```

---

# Transforms

Transforms reshape an image spatially.

---

# Slice

Splits an image into vertical slices.

## Python Example

```python
import pyctorial as px

img = px.load("image.png")

slices = px.slice(img, slices=8)

for i, s in enumerate(slices):
    px.save(s, f"slice_{i}.png")
```

### Parameters

| Parameter | Description               |
| --------- | ------------------------- |
| `slices`  | Number of vertical slices |

---

# Gradient Stretch

Expands an image horizontally by interpolating columns.

Useful for **generative distortions**.

## Python Example

```python
img = px.load("gradient.png")

stretch = px.gradient_stretch(
    img,
    x_start=300,
    width_multiplier=2.0
)

px.save(stretch, "stretched.png")
```

### Parameters

| Parameter          | Description                    |
| ------------------ | ------------------------------ |
| `x_start`          | Column where stretching begins |
| `width_multiplier` | How much to expand width       |
| `base_spacing`     | Initial anchor spacing         |
| `growth_base`      | Exponential growth factor      |
| `max_anchors`      | Maximum anchor points          |

---

# Command Line Interface

pyctorial includes a **command line tool**.

```
pyctorial COMMAND [OPTIONS]
```

---

# CLI: Halftone

```
pyctorial halftone input.jpg output.png
```

Options:

```
--cell-size 10
--max-dot-ratio 0.8
--invert
```

Example:

```
pyctorial halftone photo.jpg dots.png --cell-size 8
```

---

# CLI: Halftone SVG

```
pyctorial halftone-svg input.jpg output.svg
```

Example:

```
pyctorial halftone-svg portrait.jpg halftone.svg
```

---

# CLI: Noisy Gradient

```
pyctorial noisy-gradient output.png
```

Example:

```
pyctorial noisy-gradient gradient.png \
    --width 2000 \
    --height 2000 \
    --focal-points 8
```

---

# CLI: Slice

```
pyctorial slice input.png output_directory --slices 12
```

Example:

```
pyctorial slice image.png slices/ --slices 10
```

---

# CLI: Gradient Stretch

```
pyctorial gradient-stretch input.png output.png --x-start 400
```

Example:

```
pyctorial gradient-stretch gradient.png stretched.png \
    --x-start 300 \
    --width-multiplier 3
```

---

# Example Pipelines

## Halftone a Generated Gradient

```python
import pyctorial as px

img = px.noisy_gradient(1200, 800, 6)

img = px.halftone(img)

px.save(img, "gradient_halftone.png")
```

---

# Generate Multiple Gradients

```python
import pyctorial as px

for i in range(10):

    img = px.noisy_gradient(1200, 800, 6)

    px.save(img, f"gradient_{i}.png")
```

---

# Gradient Stretch Art

```python
import pyctorial as px

img = px.load("gradient.png")

img = px.gradient_stretch(img, x_start=500)

px.save(img, "abstract.png")
```

---

# Module Structure

```
pyctorial
├── filters
│   └── halftone
│
├── generate
│   └── noisy_gradient
│
├── transforms
│   ├── slice
│   └── gradient_stretch
│
├── io
│
└── cli
```

---

# Dependencies

pyctorial relies on several libraries:

* Pillow
* NumPy
* noise
* scipy
* tqdm

These will automatically install with pip.

---

# Contributing

Contributions are welcome.

Possible areas:

* new pattern generators
* image filters
* geometric distortions
* color tools
* GPU acceleration

---

# License

MIT License

---

# Future Ideas

Possible future features:

* Voronoi patterns
* Flow fields
* Reaction diffusion textures
* Fractal noise generators
* Tiling generators
* Image dithering
* Color palette utilities
* Node-based pipelines

---

# Summary

pyctorial is intended as a **lightweight generative image toolkit** combining:

* procedural pattern generation
* image filters
* spatial transforms
* CLI utilities

It is ideal for:

* generative art
* image experimentation
* creative coding
* automated graphics pipelines

---

Enjoy creating with **pyctorial**.
