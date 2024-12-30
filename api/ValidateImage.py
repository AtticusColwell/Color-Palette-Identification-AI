import numpy as np
import cv2
import json
from fastapi import FastAPI, File, UploadFile

# Define constants
BRIGHTNESS_THRESHOLD = (100, 300)  # Luminance range
COLOR_TEMP_RANGE = (0, 555)  # Kelvin range
CONTRAST_THRESHOLD = 50  # Minimum contrast difference

# Initialize FastAPI
app = FastAPI()

def preprocess_image(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return lab, hsv

def analyze_lighting(lab, hsv):
    l_channel = lab[:, :, 0]
    mean_brightness = np.mean(l_channel)
    contrast = np.max(l_channel) - np.min(l_channel)
    b_channel = lab[:, :, 2]
    mean_hue = np.mean(b_channel)
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
        feedback.append("Lighting appears too warm (yellowish).")
    if uniformity > 75:
        feedback.append("Lighting is uneven. Avoid shadows or highlights.")
    return len(feedback) == 0, feedback

@app.post("/validate-lighting")
async def validate_lighting(file: UploadFile = File(...)):
    try:
        # Read uploaded image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return {"error": "Invalid image file"}

        # Process and analyze the image
        lab, hsv = preprocess_image(image)
        mean_brightness, contrast, mean_hue, uniformity = analyze_lighting(lab, hsv)
        valid, feedback = validate_lighting_lab(mean_brightness, contrast, mean_hue, uniformity)

        # Return results
        return {
            "valid": valid,
            "feedback": feedback
        }
    except Exception as e:
        return {"error": str(e)}
