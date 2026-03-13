from PIL import Image

def load(path: str, mode=None) -> Image.Image:
    img = Image.open(path)
    if mode:
        img = img.convert(mode)
    return img


def save(img: Image.Image, path: str):
    img.save(path)