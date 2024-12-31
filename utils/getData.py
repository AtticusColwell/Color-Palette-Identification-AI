import os
import numpy as np
import cv2
import torch
from torchvision import transforms
from utils.model import BiSeNet  # Import BiSeNet model
from utils.undertone_analysis import classify_tone  # Import undertone classification logic

# Preload the BiSeNet model globally
n_classes = 19
net = BiSeNet(n_classes=n_classes)
checkpoint = torch.load('res/cp/79999_iter.pth', map_location=torch.device('cpu'), weights_only=False)
net.load_state_dict(checkpoint)
net.to("cpu")
net.eval()

# Preprocessing transformation
to_tensor = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])
def validate_image(image):
    if len(image.shape) != 3 or image.shape[-1] != 3:
        raise ValueError("Input image must be RGB with 3 channels.")
    print("as\ndfdsafjsad;l\nkfjsdlak;fjsdal;kfjsdalkfjsdalfj\nasdfdsafdfdsafasdfads\n")



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
    Expects an opened image and parsing mask.
    Returns the undertone: warm, cool, neutral.
    """
    # Define the neck mask
    neck_mask = (parsing == 14)  # Neck mask
    neck_pixels = image[neck_mask]
    
    # Check if the neck mask is sufficiently large
    min_neck_pixels = 500  # Define a threshold for a "reasonable" size
    if neck_pixels.size < min_neck_pixels:
        # Switch to the skin mask if neck mask is too small
        print("Neck mask too small, switching to skin mask.")
        skin_mask = (parsing == 1)  # Skin mask
        skin_pixels = image[skin_mask]
        
        # Check if the skin mask has valid pixels
        if skin_pixels is None or skin_pixels.size == 0:
            raise ValueError("No skin pixels found in the mask.")
        else:
            # Create a masked image for the skin
            skin_masked_image = np.zeros_like(image)
            skin_masked_image[skin_mask] = image[skin_mask]
            skin_masked_image_bgr = cv2.cvtColor(skin_masked_image, cv2.COLOR_RGB2BGR)



            # Compute the tone using the skin mask
            tone = classify_tone(skin_masked_image_bgr)
            return tone
    else:
        # Create a masked image for the neck
        masked_image = np.zeros_like(image)  # Create a black image
        masked_image[neck_mask] = image[neck_mask]  # Apply the masked pixels
        masked_image_bgr = cv2.cvtColor(masked_image, cv2.COLOR_RGB2BGR)





        # Compute the tone using the neck mask
        tone = classify_tone(masked_image_bgr)
        return tone
    
def extract_features(image):

    """
    Extract features (hair color, eye color, skin color, undertones) from a single image.

    Args:
        image (np.ndarray): Input image in RGB format.

    Returns:
        dict: Extracted features including colors and undertones.
    """

    

    try:
        print(f"Input image shape: {image.shape}")
        # Resize image for consistent processing
        resized_image = cv2.resize(image, (512, 512))
        print("Resized image shape:", resized_image.shape)

        # Convert to tensor and process with BiSeNet
        img_tensor = to_tensor(resized_image).unsqueeze(0)
        print("Tensor shape:", img_tensor.shape)
        with torch.no_grad():
            output = net(img_tensor)[0]
        print("Model output shape:", output.shape)
        
        parsing = output.squeeze(0).cpu().numpy().argmax(0)  # Parsing map
        print("Parsing map unique values:", np.unique(parsing))

        neck_mask = (parsing == 14)
        if not np.any(neck_mask):
            neck_mask = (parsing == 1)

        # Extract features
        hair_color = get_median_color(resized_image, (parsing == 17))  # Hair mask
        print("Hair Color:", hair_color)
        eye_color = get_median_color(resized_image, (parsing == 5))   # Eye mask
        print("eye_color:", eye_color)
        skin_color = get_median_color(resized_image, neck_mask)  # Neck mask
        print("skin_color:", skin_color)
        undertones = get_undertones(resized_image, parsing)
        print("undertones:", undertones)

        return {
            "hair_color": hair_color,
            "eye_color": eye_color,
            "skin_color": skin_color,
            "undertone": undertones,
        }

    except Exception as e:
        raise ValueError(f"Error in feature extraction: {e}")
