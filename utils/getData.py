import os
import numpy as np
import cv2
import torch
from torchvision import transforms
from model import BiSeNet  # Import BiSeNet model
from UnderToneAnalysis import classify_tone  # Import undertone classification logic

# Preload the BiSeNet model globally
n_classes = 19
net = BiSeNet(n_classes=n_classes)
checkpoint = torch.load('res/cp/79999_iter.pth', map_location=torch.device('cpu'))
net.load_state_dict(checkpoint)
net.to("cpu")
net.eval()

# Preprocessing transformation
to_tensor = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])

def get_median_color(image, mask):
    """
    Compute the median RGB color for a given mask.
    """
    pixels = image[mask]
    if pixels.size == 0:
        
        raise ValueError("No pixels found in the mask.")
    return np.median(pixels, axis=0).tolist()

def get_undertones(image, parsing):
    """
    Determine undertones using neck or skin regions from the parsing mask.
    """
    neck_mask = (parsing == 14)  # Neck mask
    neck_pixels = image[neck_mask]

    # If neck mask is too small, fallback to skin mask
    if neck_pixels.size < 500:
        skin_mask = (parsing == 1)  # Skin mask
        skin_pixels = image[skin_mask]
        if skin_pixels.size == 0:
            raise ValueError("No skin pixels found.")
        return classify_tone(skin_pixels)
    return classify_tone(neck_pixels)

def extract_features(image):
    """
    Extract features (hair color, eye color, skin color, undertones) from a single image.

    Args:
        image (np.ndarray): Input image in RGB format.

    Returns:
        dict: Extracted features including colors and undertones.
    """
    try:
        # Resize image for consistent processing
        resized_image = cv2.resize(image, (512, 512))

        # Convert to tensor and process with BiSeNet
        img_tensor = to_tensor(resized_image).unsqueeze(0)
        with torch.no_grad():
            output = net(img_tensor)[0]
        parsing = output.squeeze(0).cpu().numpy().argmax(0)  # Parsing map
        neck_mask = (parsing == 14)
        if not np.any(neck_mask):
            neck_mask = (parsing == 1)

        # Extract features
        hair_color = get_median_color(resized_image, (parsing == 17))  # Hair mask
        eye_color = get_median_color(resized_image, (parsing == 5))   # Eye mask
        skin_color = get_median_color(resized_image, neck_mask)  # Neck mask
        undertones = get_undertones(resized_image, parsing)

        return {
            "hair_color": hair_color,
            "eye_color": eye_color,
            "skin_color": skin_color,
            "undertone": undertones,
        }

    except Exception as e:
        raise ValueError(f"Error in feature extraction: {e}")
