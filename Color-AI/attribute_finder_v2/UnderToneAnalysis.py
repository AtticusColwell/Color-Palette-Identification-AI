import numpy as np
import cv2




def process_image(image):
    
    
    #convert BRG image to lab
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    #extract a and b channels
    a_channel = lab_image[:, :, 1]
    b_channel = lab_image[:, :, 2]

    return a_channel, b_channel



def detect_undertone(a_channel, b_channel):

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
    # Convert OpenCV Lab to theoretical Lab (pixel-wise)
    a = a_channel - 128
    b = b_channel - 128

    # Compute pixel-wise hue and chroma
    hue_angles = np.degrees(np.arctan2(b, a))
    hue_angles[hue_angles < 0] += 360  # Normalize to [0°, 360°]
    chroma = np.sqrt(a**2 + b**2)

    # Compute mean hue and chroma
    mean_hue = np.mean(hue_angles)
    print( mean_hue)
    mean_chroma = np.mean(chroma)
    print( mean_chroma)

    # Classify tone
    if mean_chroma < 5:  # Adjusted neutral threshold
        tone = "Neutral"
    elif 0 <= mean_hue <= 50 or 320 <= mean_hue <= 360:  # Narrow warm range
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
        a_channel, b_channel = process_image(image)
        
        
        # Detect the undertone
        tone, _, _ = detect_undertone(a_channel, b_channel)
        return tone
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")


# Only run the main function if executed directly
if __name__ == "__main__":
    # Example usage for standalone testing
    
    
    
    # Load an image for testing
    image = cv2.imread("../ImageInput/undertoneImgs/coolneck.png")
    if image is None:
        raise ValueError("Invalid image file")
    
    # Classify the tone
    tone = classify_tone(image)
    print(f"Detected Tone: {tone}")

