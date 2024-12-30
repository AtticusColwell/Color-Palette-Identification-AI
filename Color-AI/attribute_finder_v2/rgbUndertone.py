import cv2
import numpy as np

def load_image(image_path):
    image_bgr = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return image_rgb

def detect_rgb_warmth(image):
    # Ensure the image is in RGB format
    if image.shape[-1] == 3:
        r_channel = image[:, :, 0]
        g_channel = image[:, :, 1]
        b_channel = image[:, :, 2]
    else:
        raise ValueError("Input image must have 3 channels (RGB).")

    # Calculate mean values for R, G, B
    mean_r = np.mean(r_channel)
    mean_g = np.mean(g_channel)
    mean_b = np.mean(b_channel)

    # Calculate warmth index
    warmth_index = mean_r / (mean_b + 1e-5)  # Avoid division by zero

    # Classify tone based on thresholds
    if warmth_index > 1.2 and mean_r > mean_g > mean_b:
        tone = "Warm"
    elif warmth_index < 0.8 and mean_b > mean_g > mean_r:
        tone = "Cool"
    else:
        tone = "Neutral"

    return tone, warmth_index, mean_r, mean_g, mean_b

def main(image_path):
    try:
        image = load_image(image_path)
        tone, _, _, _, _, = detect_rgb_warmth(image)
        print(tone)
    except Exception as e:
        print(f"Error: {e}")

# Example usage
main("../ImageInput/undertoneImgs/coolneck.png")