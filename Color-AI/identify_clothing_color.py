import cv2
import numpy as np

def remove_white_background_and_get_median(
    img: np.ndarray,
    white_threshold: int = 250,
    make_transparent: bool = False
):
    """
    1. Conservatively remove near-white pixels.
    2. Compute the median color of the remaining region.

    Parameters:
    -----------
    img : np.ndarray
        BGR image loaded by OpenCV.
    white_threshold : int
        Pixel is considered "white" if R, G, B >= this value.
        The higher the threshold, the fewer pixels are removed.
    make_transparent : bool
        If True, output image will have an alpha channel for removed background.
        Otherwise, removed background will be black.

    Returns:
    --------
    result_img : np.ndarray
        The image with background removed (black or transparent).
    median_color_bgr : tuple
        The median color (B, G, R) of the non-white region.
    """

    # --- 1. Create a mask of white pixels ----------------------------------
    lower_bound = np.array([white_threshold, white_threshold, white_threshold], dtype=np.uint8)
    upper_bound = np.array([255, 255, 255], dtype=np.uint8)
    mask_white = cv2.inRange(img, lower_bound, upper_bound)

    # Invert the mask to get the "subject" mask (non-white)
    subject_mask = cv2.bitwise_not(mask_white)

    # --- 2. Remove background ----------------------------------------------
    if not make_transparent:
        # Make the background black
        result_img = cv2.bitwise_and(img, img, mask=subject_mask)
    else:
        # Create a 4-channel BGRA image
        b, g, r = cv2.split(img)
        alpha = subject_mask
        result_img = cv2.merge((b, g, r, alpha))

    # --- 3. Compute median color of the subject region ----------------------
    subject_pixels = img[subject_mask == 255]

    if len(subject_pixels) == 0:
        median_color_bgr = (0, 0, 0)
    else:
        median_b = np.median(subject_pixels[:, 0])
        median_g = np.median(subject_pixels[:, 1])
        median_r = np.median(subject_pixels[:, 2])
        median_color_bgr = (int(median_b), int(median_g), int(median_r))

    return result_img, median_color_bgr

def process_image(input_path: str, output_path: str = None, make_transparent: bool = False):
    """
    Process an image by removing the white background and computing the median color.

    Parameters:
    -----------
    input_path : str
        Path to the input image.
    output_path : str, optional
        Path to save the processed image. If None, the image will not be saved.
    make_transparent : bool
        If True, the output image will have a transparent background.

    Returns:
    --------
    result_img : np.ndarray
        The processed image with the white background removed.
    median_color_rgb : tuple
        The median color of the non-white region in (R, G, B).
    """
    # Load the image
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Could not read image from '{input_path}'")

    # Remove white background and compute median color
    result, median_bgr = remove_white_background_and_get_median(
        img, 
        white_threshold=250, 
        make_transparent=make_transparent
    )

    # Print median color
    median_b, median_g, median_r = median_bgr
    median_color_rgb = (median_r, median_g, median_b)
    print(f"Median color (RGB) = {median_color_rgb}")

    # Save result if an output path is specified
    if output_path:
        cv2.imwrite(output_path, result)
        print(f"Processed image saved to: {output_path}")

    return result, median_color_rgb

# Example usage
if __name__ == "__main__":
    input_path = "photos/clothes/image1.png"
    output_path = "output.png"  # Optional: Provide an output path if you want to save the result
    processed_image, median_color = process_image(input_path, output_path)
    print(f"Median color of the processed image: {median_color}")

