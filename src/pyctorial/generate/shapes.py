from PIL import Image, ImageDraw
import random

def increasing_squares(width, height, cell_size = 20, color=(0, 0, 0, 255)):
    # -------- SETTINGS --------
    WIDTH = width
    HEIGHT = height
    CELL_SIZE = cell_size
    # --------------------------

    cols = WIDTH // CELL_SIZE
    rows = HEIGHT // CELL_SIZE

    # Create transparent image
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for col in range(cols):
        # probability increases from 0 -> 1 across the width
        prob = col / (cols - 1)

        for row in range(rows):
            if random.random() < prob:
                x0 = col * CELL_SIZE
                y0 = row * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE

                draw.rectangle((x0, y0, x1, y1), fill=color)

    return img