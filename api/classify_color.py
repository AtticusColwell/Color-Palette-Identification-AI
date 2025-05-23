from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel
import numpy as np
from PIL import Image
from utils.identify_clothing_color import process_image_with_combined_method
from utils.color_difference import color_is_allowed
from io import BytesIO
import json
app = FastAPI()

@app.post("/api/classify_color")
async def classify_season_api(file: UploadFile = File(...), season_dict: str = Form(...)):
    """
    Serverless function to classify a season based on an uploaded image.
    """
    print(season_dict)
    try:
        print(f"Received file: {file.filename}")
        # Read the uploaded image file
        contents = await file.read()

        season = json.loads(season_dict)
        print(season)
        season = season["season"]
        print("HERE: ", season)
        

        pil_image = Image.open(BytesIO(contents)).convert("RGB")
        print("PIL Image Mode:", pil_image.mode)  # Debug print

        image_np = np.array(pil_image)
        print("Image Shape:", image_np.shape)  # Debug print
        
        if image_np is None or len(image_np.shape) != 3 or image_np.shape[-1] != 3:  # Validate the image
            raise ValueError("Invalid image file or incorrect number of channels (not RGB).")

        
        clothing_color = process_image_with_combined_method(image_np)
        print("Clothing Color:", clothing_color)  # Debug print

        if clothing_color is None or len(clothing_color) != 3:
            raise ValueError("Could not identify clothing color.")
        
        print("identifying clothing color exited sucessfully")

        allowed = color_is_allowed(clothing_color, season)
        print(allowed)
        print(clothing_color)
        return{
            "color is allowed (T/F)": allowed,
            "message": "Color identification successful."
        }
        #TODO: Would like to have
        # return{
        #     "color is allowed (T/F)": allowed,
        #     "RGB value of clothing": list(clothing_color),
        #     "message": "Color identification successful."
        # }
    except Exception as e:
        return {"error": str(e)}
        


