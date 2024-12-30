import numpy as np
import cv2

BRIGHTNESS_THRESHOLD = (100, 300)  # Luminance range
COLOR_TEMP_RANGE = (0, 555)  # Kelvin range
CONTRAST_THRESHOLD = 50  # Minimum contrast difference


def load_image(file_path):
    """
    Loads in the image using openCV then converts from standard 

    Args:
        param1 (type): Description of the first parameter.
        param2 (type): Description of the second parameter.

    Returns:
        type: Description of the return value.
    """
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError("Invalid image file")
    return image


def preprocess_image(image):
    """
    Converts the image from standard BGR color space(default when openCV loads it in) to both the lab and hsv colorspaces

    a lab in openCV is a color representation model that seperates color information into three components
        
        L (Lightness): Represents the brightness of the color, ranging from 0 (black) to 100 (white).
        a (Green-Red): Represents the position between green and red. Negative values indicate green, and positive values indicate red.
        b (Blue-Yellow): Represents the position between blue and yellow. Negative values indicate blue, and positive values indicate yellow.

    the utiility of converting to the lab color space is the seperation of factors like brightness from that of hue. This works for our purposes as we need to correct seperatley
    for overly bright photos vs ones with bad color contrast. 

    hsv is the hue saturation value color space. hsv seperates the color information into three parts. 
        1. Hue, representing color type, normally goes from 0 to 360 degrees but is normalized to [0-179] in openCV for 8 bit representation
        2. Saturation, is stored as a value from 0 to 255 where 0 is total greyscale and 255 is total saturation
        3. value represents the brightness of the color, vlaues ranging from 0 to 255
    
    Simlilar to the lab colorspace, the utility of the hsv color space for us is the seperation of information like color type from brightness. This space lets us threshhold
    seeing if an image is within a color range, and hue seperated from brightness helps us determin color with less variablility based on light. 
    

    Args:
        param1 (type): Description of the first parameter.
        

    Returns:
        type: Description of the return value.
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return lab, hsv

def analyze_lighting(lab, hsv):
    # Brightness
    l_channel = lab[:, :, 0]
    mean_brightness = np.mean(l_channel)

    # Contrast
    contrast = np.max(l_channel) - np.min(l_channel)

    # Color Temperature (approximation via b channel)
    b_channel = lab[:, :, 2]
    mean_hue = np.mean(b_channel)  # Higher values indicate warmer lighting


    # Uniformity
    uniformity = np.std(l_channel)

    return mean_brightness, contrast, mean_hue, uniformity

def validate_lighting_lab(mean_brightness, contrast, mean_b, uniformity):
    feedback = []
    if not (BRIGHTNESS_THRESHOLD[0] <= mean_brightness <= BRIGHTNESS_THRESHOLD[1]):
        feedback.append("Adjust brightness to fall within the acceptable range.")
    if contrast < CONTRAST_THRESHOLD:
        feedback.append("Increase contrast by improving lighting.")
    if mean_b < COLOR_TEMP_RANGE[0]:  # Cooler tones
        feedback.append("Lighting appears too cool (bluish).")
    elif mean_b > COLOR_TEMP_RANGE[1]:  # Warmer tones (threshold can be adjusted)
        print(mean_b)
        feedback.append("Lighting appears too warm (yellowish).")
    if uniformity > 75:  # Adjust based on testing
        feedback.append("Lighting is uneven. Avoid shadows or highlights.")

    return len(feedback) == 0, feedback


   
def provide_feedback(valid, feedback):
    if valid:
        print("Lighting conditions are acceptable.")
    else:
        print("Lighting conditions are not acceptable. Suggestions:")
        for issue in feedback:
            print(f"- {issue}")


def main(image_path):
    try:
        image = load_image(image_path)
        lab, hsv = preprocess_image(image)
        mean_brightness, contrast, mean_hue, uniformity = analyze_lighting(lab, hsv)
        valid, feedback = validate_lighting_lab(mean_brightness, contrast, mean_hue, uniformity)
        provide_feedback(valid, feedback)
    except Exception as e:
        print(f"Error: {e}")

# Example usage
main("../photos/faces/valid_face_3.png")





