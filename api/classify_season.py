from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from PIL import Image
from utils.getData import extract_features
from utils.classify import classify_season

app = FastAPI()


app.post("/api/classify_season")
async def classify_season_api(file: UploadFile = File(...)):
    """
    Serverless function to classify a season based on an uploaded image.
    """
    try:
        # Read the uploaded image file
        contents = await file.read()

        pil_image = Image.open(contents).convert("RGB")

        image_np = np.array(pil_image)
        if image_np is None:
            raise ValueError("Invalid image file")
        if pil_image is None:
            raise ValueError("Invalid image file")
        
        features = extract_features(image_np)

        skin_rgb = features["skin_color"]
        hair_rgb = features["hair_color"]
        eye_rgb = features["eye_color"]
        tone = features["undertone"]

        season = classify_season(skin_rgb, hair_rgb, eye_rgb, tone)

        return{
            "season": season,
            "message": "Color season classification successful."
        }
    except Exception as e:
        return {"error": str(e)}
        


