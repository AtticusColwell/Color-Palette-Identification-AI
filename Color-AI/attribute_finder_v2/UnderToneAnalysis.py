import numpy as np
import cv2



def process_image(image):
    '''
    Processes the input image by converting it to the LAB color space and extracting
    the 'a' and 'b' channels for chromaticity analysis.
    
    Args:
        image (np.ndarray): Input image in BGR format.

    Returns:
        tuple: A tuple containing:
            - a_channel (np.ndarray): The 'a' channel of the LAB image.
            - b_channel (np.ndarray): The 'b' channel of the LAB image.
            - mask (np.ndarray): Binary mask to exclude invalid pixels.
    '''
    #convert BRG image to lab
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    #extract a and b channels
    a_channel = lab_image[:, :, 1]
    b_channel = lab_image[:, :, 2]

    mask = cv2.inRange(image, (1, 1, 1), (255, 255, 255))

    return a_channel, b_channel, mask



def detect_undertone(a_channel, b_channel, mask):

    """
        hue angle lets us classify tones based on color theory using formula
                    HueAngle(θ) = arctan(a/b)*180/π
        Hue angle ranges based on color theory
        Warm tones: θ ∈[0,60]∪[300∘,360∘]
        Cool Tones: θ ∈[60, 300]
        Neutral Tones: Not explicitly defined through hue but by low chroma in either direction

        Chroma provides an objective measure of how far the the tone is from true neutral
        Regardless of if the tone falls into the cool or warm range, if the chroma is below a threshold it
        is neutral
                            Chroma =  (a^2 + b^2)^0.5
    """
    # Convert OpenCV LAB to theoretical LAB (pixel-wise)
    a = (a_channel - 128).astype(np.float32)
    b = (b_channel - 128).astype(np.float32)

    # Compute pixel-wise hue and chroma
    hue_angles = np.degrees(np.arctan2(b, a))
    hue_angles[hue_angles < 0] += 360  # Normalize to [0°, 360°]
    chroma = np.sqrt(a**2 + b**2)

    # Apply the mask to exclude black pixels
    valid_hue = hue_angles[mask > 0]
    valid_chroma = chroma[mask > 0]

    # Compute mean hue and chroma only for valid pixels
    mean_hue = np.mean(valid_hue) if valid_hue.size > 0 else 0
    mean_chroma = np.mean(valid_chroma) if valid_chroma.size > 0 else 0

    # Classify tone
    if mean_chroma < 5:  # Adjusted neutral threshold
        tone = "Neutral"
    elif 0 <= mean_hue <= 69 or 300 <= mean_hue <= 360:  # Narrow warm range
        tone = "Warm"
    else:
        tone = "Cool"

    return tone, mean_chroma, mean_hue

def classify_tone(image):
    """
    Classifies the undertone of an image as Warm, Cool, or Neutral.

    Args:
        image (np.ndarray): The input image in RGB format.

    Returns:
        str: The detected tone (Warm, Cool, Neutral).
    """
    try:
        # Process the image to extract Lab channels
        a_channel, b_channel, mask = process_image(image)
        
        
        # Detect the undertone
        tone, chroma, hue = detect_undertone(a_channel, b_channel, mask)
        print(chroma)
        print(hue)
        return tone
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")


# Only run the main function if executed directly
if __name__ == "__main__":
    # Example usage for standalone testing
    
    
    
    # Load an image for testing
    image = cv2.imread("../ImageInput/undertoneImgs/warmneck.png")
    if image is None:
        raise ValueError("Invalid image file")
    
    # Classify the tone
    tone = classify_tone(image)
    print(f"Detected Tone: {tone}")

