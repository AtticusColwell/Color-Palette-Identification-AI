import numpy as np
import cv2


def process_image(image):
    """
    Converts an image to LAB color space and extracts the A and B channels
    along with a mask to filter valid pixels.

    Args:
        image (np.ndarray): Input image in BGR format.

    Returns:
        tuple: A-channel, B-channel, and mask of valid pixels.
    """
    print("image shape recived:", image.shape)
    # Convert BGR image to LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    a_channel = lab_image[:, :, 1]
    b_channel = lab_image[:, :, 2]

    # Create a mask for valid pixels
    mask = cv2.inRange(image, (1, 1, 1), (255, 255, 255))

    return a_channel, b_channel, mask


def detect_undertone(a_channel, b_channel, mask):
    """
    Detects the undertone of an image region using LAB color theory.

    Args:
        a_channel (np.ndarray): A-channel of LAB image.
        b_channel (np.ndarray): B-channel of LAB image.
        mask (np.ndarray): Mask to exclude invalid pixels.

    Returns:
        tuple: Tone classification ('Warm', 'Cool', 'Neutral'), mean chroma, mean hue.
    """
    # Convert channels to float32 and center around 0
    a = (a_channel - 128).astype(np.float32)
    b = (b_channel - 128).astype(np.float32)

    # Compute hue angles and chroma
    hue_angles = np.degrees(np.arctan2(b, a))
    hue_angles[hue_angles < 0] += 360  # Normalize hue to [0, 360]
    chroma = np.sqrt(a**2 + b**2)

    # Apply the mask to exclude invalid pixels
    valid_hue = hue_angles[mask > 0]
    valid_chroma = chroma[mask > 0]

    # Compute mean hue and chroma for valid pixels
    mean_hue = np.mean(valid_hue) if valid_hue.size > 0 else 0
    mean_chroma = np.mean(valid_chroma) if valid_chroma.size > 0 else 0

    # Classify tone based on mean hue and chroma
    if mean_chroma < 5:  # Threshold for neutral tones
        tone = "Neutral"
    elif 0 <= mean_hue <= 69 or 300 <= mean_hue <= 360:  # Warm tone ranges
        tone = "Warm"
    else:  # Remaining range is cool
        tone = "Cool"

    return tone, mean_chroma, mean_hue


def classify_tone(image):
    """
    Classifies the undertone of an image as Warm, Cool, or Neutral.

    Args:
        image (np.ndarray): The input image in RGB format.

    Returns:
        str: The detected tone ('Warm', 'Cool', 'Neutral').
    """
    print("starting undertone_analysis function")
    
    try:
        # Process the image to extract LAB channels and mask
        a_channel, b_channel, mask = process_image(image)

        # Detect the undertone
        tone, chroma, hue = detect_undertone(a_channel, b_channel, mask)

        return tone
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")
