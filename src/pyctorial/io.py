from PIL import Image
import os

def load(path: str, mode=None) -> Image.Image:
    img = Image.open(path)
    if mode:
        img = img.convert(mode)
    return img


def save(img: Image.Image, path: str):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    img.save(path)

def save_svg(svg_string, path):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w") as f:
        f.write(svg_string)