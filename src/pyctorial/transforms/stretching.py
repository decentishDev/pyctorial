from PIL import Image
import numpy as np
from tqdm import tqdm

def gradient_stretch(
    img: Image.Image,
    x_start: int,
    width_multiplier: float = 2.0,
    base_spacing: int = 1,
    growth_base: int = 2,
    max_anchors: int = 40,
    show_progress: bool = True,
):
    src = np.array(img, dtype=np.float32)

    h, w, c = src.shape
    new_w = int(w * width_multiplier)

    out = np.zeros((h, new_w, c), dtype=np.float32)

    # Copy left side INCLUDING x_start
    out[:, :x_start + 1] = src[:, :x_start + 1]

    # --- Generate integer exponential anchors ---
    anchors = [x_start]
    delta = max(1, int(base_spacing))

    for _ in range(max_anchors - 1):
        next_pos = anchors[-1] + delta
        if next_pos >= new_w:
            break
        anchors.append(next_pos)
        delta *= growth_base

    # Ensure final anchor reaches right edge
    if anchors[-1] < new_w:
        anchors.append(new_w)

    iterator = tqdm(range(len(anchors) - 1), desc="Stretching") \
        if show_progress else range(len(anchors) - 1)

    for i in iterator:
        out_x0 = int(anchors[i])
        out_x1 = int(anchors[i + 1])

        span = int(out_x1 - out_x0)
        if span <= 0:
            continue

        src_x0 = min(x_start + i, w - 1)
        src_x1 = min(x_start + i + 1, w - 1)

        col0 = src[:, src_x0]
        col1 = src[:, src_x1]

        for dx in range(span):
            t = dx / span
            out[:, out_x0 + dx] = (1 - t) * col0 + t * col1

    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))