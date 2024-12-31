import cv2
import numpy as np

def remove_white_background_and_get_median(
    img: np.ndarray,
    white_threshold: int = 250,
    make_transparent: bool = False
):
    """
    Remove near-white pixels and compute the median color of the remaining region.

    Parameters:
    -----------
    img : np.ndarray
        RGB image loaded by OpenCV.
    white_threshold : int
        Pixel is considered "white" if R, G, B >= this value.
    make_transparent : bool
        If True, output image will have an alpha channel for removed background.

    Returns:
    --------
    result_img : np.ndarray
        The image with background removed (black or transparent).
    median_color_rgb : tuple
        The median color (R, G, B) of the non-white region.
    """

    lower_bound = np.array([white_threshold, white_threshold, white_threshold], dtype=np.uint8)
    upper_bound = np.array([255, 255, 255], dtype=np.uint8)
    mask_white = cv2.inRange(img, lower_bound, upper_bound)

    subject_mask = cv2.bitwise_not(mask_white)

    if not make_transparent:
        result_img = cv2.bitwise_and(img, img, mask=subject_mask)
    else:
        r, g, b = cv2.split(img)
        alpha = subject_mask
        result_img = cv2.merge((r, g, b, alpha))

    subject_pixels = img[subject_mask == 255]

    if len(subject_pixels) == 0:
        median_color_rgb = (0, 0, 0)
    else:
        median_r = np.median(subject_pixels[:, 0])
        median_g = np.median(subject_pixels[:, 1])
        median_b = np.median(subject_pixels[:, 2])
        median_color_rgb = (int(median_r), int(median_g), int(median_b))

    return result_img, median_color_rgb

def get_shirt_base_color_kmeans(img_rgb, median_color_rgb, k=4, crop=None):
    """
    Use k-means clustering to find the dominant color closest to the median color.

    Parameters:
    -----------
    image_path : str
        Path to the input image.
    median_color_rgb : tuple
        The median color (R, G, B) from the previous step.
    k : int
        Number of clusters for k-means.
    crop : tuple, optional
        Region to crop as (x, y, w, h).

    Returns:
    --------
    closest_color_rgb : tuple
        The cluster center (R, G, B) closest to the median color.
    """
    if crop is not None:
        x, y, w, h = crop
        img_rgb = img_rgb[y:y+h, x:x+w]

    pixels = img_rgb.reshape(-1, 3).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    distances = np.linalg.norm(centers - np.array(median_color_rgb), axis=1)
    closest_idx = np.argmin(distances)
    closest_color_rgb = centers[closest_idx].astype(int)

    return tuple(closest_color_rgb)

def process_image_with_combined_method(img_rgb, output_path: str = None, k=4, crop=None):
    """
    Process an image by removing the white background, finding the median color,
    and identifying the dominant k-means cluster closest to the median color.

    Parameters:
    -----------
    input_path : str
        Path to the input image.
    output_path : str, optional
        Path to save the processed image.
    k : int
        Number of clusters for k-means.
    crop : tuple, optional
        Region to crop as (x, y, w, h).

    Returns:
    --------
    result_img : np.ndarray
        The processed image with the white background removed.
    closest_color_rgb : tuple
        The closest k-means cluster center to the median color (R, G, B).
    """
    print("starting process_image_with_combined_method")
    try:
        result, median_color_rgb = remove_white_background_and_get_median(img_rgb)

        closest_color_rgb = get_shirt_base_color_kmeans(
            img_rgb, median_color_rgb, k=k, crop=crop
        )

        if output_path:
            result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, result_bgr)
            print(f"Processed image saved to: {output_path}")

        print(f"Median color (RGB): {median_color_rgb}")
        print(f"Closest color (RGB): {closest_color_rgb}")

        return closest_color_rgb
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")

# # Example usage
# if __name__ == "__main__":
#     input_path = "photos/clothes/image2.png"
#     output_path = "output.png"  # Optional
#     processed_image, closest_color = process_image_with_combined_method(input_path, output_path, k=5)
#     print(f"Closest color to the median (RGB): {closest_color}")

