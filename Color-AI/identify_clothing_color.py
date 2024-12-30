"""
Identify the dominant (base) color of a garment in an image.

Steps:
1. Remove the background using 'rembg'.
2. Extract the dominant color with 'colorthief'.

Usage:
    python get_dominant_color.py --input path/to/clothing_image.jpg --output output.png
"""

import argparse
import os
from colorthief import ColorThief
from io import BytesIO
from PIL import Image
import backgroundremover

backgroundremover.remove_background_from_img_file(
    input_path="clothing.jpg",
    output_path="clothing_nobg.png"
)

def remove_background(input_path: str, output_path: str) -> None:
    """
    Removes the background from the input image and saves the result to output_path.
    """
    # Read original image
    with open(input_path, 'rb') as f:
        input_bytes = f.read()
    
    # Remove the background
    result_bytes = remove(input_bytes)
    
    # Save the background-removed image
    with open(output_path, 'wb') as f:
        f.write(result_bytes)


def get_dominant_color(image_path: str, quality: int = 1):
    """
    Returns the dominant color of the image as an (R, G, B) tuple.

    'quality' is an optional parameter in ColorThief:
    - Lower quality (1) is faster but less accurate.
    - Higher quality means more pixel sampling (slower).
    """
    color_thief = ColorThief(image_path)
    # get_color returns the dominant color in (R, G, B)
    return color_thief.get_color(quality=quality)


def colors(input_path):    
    # 1. Remove background
    print(f"Removing background from {input_path}...")
    remove_background(input_path, output_path)

    

    # 2. Compute dominant color
    print(f"Extracting dominant color from {output_path}...")
    dominant_color = get_dominant_color(output_path, quality=1)
    
    print(f"Dominant (base) color is: {dominant_color} (R, G, B)")


if __name__ == "__main__":
    main()
