import numpy as np
from PIL import Image
from noise import pnoise2
from scipy.ndimage import gaussian_filter
from tqdm import tqdm
import random

def noisy_gradient(
    width,
    height,
    num_focal_points,
    blur_strength=400,
    warp_strength=0.2,
):

    # --- CONFIGURATION ---
    WIDTH = width
    HEIGHT = height
    NUM_FOCAL_POINTS = num_focal_points
    BLUR_STRENGTH = blur_strength
    WARP_STRENGTH = warp_strength

    PALETTE = np.array([
        [8, 18, 22],
        [60, 100, 95],
        [110, 140, 135],
        [235, 235, 230],
        [180, 150, 100],
        [40, 60, 120]
    ]) / 255.0

    def generate_gradient():
        y, x = np.mgrid[0:HEIGHT, 0:WIDTH]
        
        canvas = np.zeros((HEIGHT, WIDTH, 3))
        weight_map = np.zeros((HEIGHT, WIDTH))

        for _ in range(NUM_FOCAL_POINTS):
            px = random.randint(0, WIDTH - 1)
            py = random.randint(0, HEIGHT - 1)

            color = random.choice(PALETTE)
            
            # Inject color into a small "patch" rather than just a pixel
            # This gives the blur a stronger starting point
            r = random.randint(20, 50)
            y_slice = slice(max(0, py-r), min(HEIGHT, py+r))
            x_slice = slice(max(0, px-r), min(WIDTH, px+r))
            
            canvas[y_slice, x_slice] += color
            weight_map[y_slice, x_slice] += 1.0

        # 3. Massive Gaussian Spread
        # This turns the small patches into the "blobs"
        for i in range(3):
            canvas[:,:,i] = gaussian_filter(canvas[:,:,i], BLUR_STRENGTH)
        weight_map = gaussian_filter(weight_map, BLUR_STRENGTH)
        
        # Normalize
        weight_map[weight_map == 0] = 1e-5
        color_field = canvas / weight_map[..., None]

        # 4. Create a SMOOTH Flow Field for the Mesh Warp
        # We use a very low scale for large, sweeping distortions
        noise_scale = 0.0016#0.0008 
        noise_x = np.zeros((HEIGHT, WIDTH))
        noise_y = np.zeros((HEIGHT, WIDTH))
        
        # Generate noise with low frequency
        for i in range(0, HEIGHT, 20):
            for j in range(0, WIDTH, 20):
                nx = pnoise2(i * noise_scale, j * noise_scale, octaves=1)
                ny = pnoise2(i * noise_scale + 50, j * noise_scale + 50, octaves=1)
                noise_x[i:i+20, j:j+20] = nx
                noise_y[i:i+20, j:j+20] = ny

        # Smooth the noise field itself to prevent "jagged" edges
        noise_x = gaussian_filter(noise_x, 50)
        noise_y = gaussian_filter(noise_y, 50)

        # 5. Apply the Warp (Displacement Mapping)
        map_x = np.clip(x + noise_x * WIDTH * WARP_STRENGTH, 0, WIDTH - 1).astype(int)
        map_y = np.clip(y + noise_y * HEIGHT * WARP_STRENGTH, 0, HEIGHT - 1).astype(int)
        color_field = color_field[map_y, map_x]

        # 6. Post-Processing: Fine Grain
        #grain = np.random.normal(0, 0.02, (HEIGHT, WIDTH, 3))
        grain = np.random.normal(0, 0.03, (HEIGHT, WIDTH, 3))
        color_field = np.clip(color_field + grain, 0, 1)

        return (color_field * 255).astype(np.uint8)

    # --- EXECUTION ---
    img_array = generate_gradient()
    return Image.fromarray(img_array)