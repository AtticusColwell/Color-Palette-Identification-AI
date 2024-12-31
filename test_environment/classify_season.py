from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from PIL import Image
from utils.getData import extract_features
from utils.classify import classify_season
from io import BytesIO

app = FastAPI()


@app.post("/classify_season")
async def classify_season_api(file: UploadFile = File(...)):
    """
    Serverless function to classify a season based on an uploaded image.
    """
    try:
        print(f"Received file: {file.filename}")
        # Read the uploaded image file
        contents = await file.read()

        pil_image = Image.open(BytesIO(contents)).convert("RGB")
        print("PIL Image Mode:", pil_image.mode)  # Debug print

        image_np = np.array(pil_image)
        print("Image Shape:", image_np.shape)  # Debug print
        
        if image_np is None or len(image_np.shape) != 3 or image_np.shape[-1] != 3:  # Validate the image
            raise ValueError("Invalid image file or incorrect number of channels (not RGB).")

        
        features = extract_features(image_np)
        print("Extracted Features:", features)  # Debug print

        skin_rgb = features["skin_color"]
        hair_rgb = features["hair_color"]
        eye_rgb = features["eye_color"]
        tone = features["undertone"]
        print("get data exited sucessfully")

        season = classify_season(skin_rgb, hair_rgb, eye_rgb, tone)

        return{
            "season": season,
            "message": "Color season classification successful."
        }
    except Exception as e:
        return {"error": str(e)}
        


