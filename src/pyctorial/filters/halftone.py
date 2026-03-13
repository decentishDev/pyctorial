import numpy as np
from PIL import Image, ImageDraw


def halftone(
    img: Image.Image,
    cell_size=12,
    max_dot_ratio=0.9,
    invert=False
) -> Image.Image:

    img = img.convert("L")
    width, height = img.size

    grid_w = width // cell_size
    grid_h = height // cell_size

    out = Image.new("RGB", (grid_w * cell_size, grid_h * cell_size), "black")
    draw = ImageDraw.Draw(out)

    pixels = np.array(img)

    for gy in range(grid_h):
        for gx in range(grid_w):

            x0 = gx * cell_size
            y0 = gy * cell_size

            region = pixels[y0:y0+cell_size, x0:x0+cell_size]
            brightness = np.mean(region) / 255.0

            if invert:
                brightness = 1 - brightness

            max_radius = (cell_size / 2) * max_dot_ratio
            radius = brightness * max_radius

            cx = x0 + cell_size / 2
            cy = y0 + cell_size / 2

            draw.ellipse(
                (cx-radius, cy-radius, cx+radius, cy+radius),
                fill="white"
            )

    return out


def halftone_svg(img, cell_size=12, max_dot_ratio=0.9, invert=False):

    img = img.convert("L")
    width, height = img.size

    pixels = np.array(img)

    grid_w = width // cell_size
    grid_h = height // cell_size

    canvas_w = grid_w * cell_size
    canvas_h = grid_h * cell_size

    circles = []

    for gy in range(grid_h):
        for gx in range(grid_w):

            x0 = gx * cell_size
            y0 = gy * cell_size

            region = pixels[y0:y0+cell_size, x0:x0+cell_size]
            brightness = np.mean(region) / 255.0

            if invert:
                brightness = 1 - brightness

            max_radius = (cell_size / 2) * max_dot_ratio
            radius = brightness * max_radius

            cx = x0 + cell_size / 2
            cy = y0 + cell_size / 2

            if radius > 0.01:
                circles.append(
                    f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="white"/>'
                )

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
width="{canvas_w}" height="{canvas_h}"
viewBox="0 0 {canvas_w} {canvas_h}">
<rect width="100%" height="100%" fill="black"/>
{''.join(circles)}
</svg>
"""

    return svg


def save_svg(svg_string, path):
    with open(path, "w") as f:
        f.write(svg_string)