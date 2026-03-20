from PIL import Image
import os

def load(path: str, mode=None) -> Image.Image:
    img = Image.open(path)
    if mode:
        img = img.convert(mode)
    return img


def save(img: Image.Image, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

def save_svg(svg_string, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg_string)