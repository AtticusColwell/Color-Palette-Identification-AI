from fastapi import FastAPI, File, UploadFile
import os
import numpy as np
from PIL import Image
import torch
from torchvision import transforms
import cv2
from UnderToneAnalysis import classify_tone
from model import BiSeNet

app = FastAPI()

# Preload the model globally
n_classes = 19
net = BiSeNet(n_classes=n_classes)
checkpoint = torch.load('res/cp/79999_iter.pth', map_location=torch.device('cpu'))
net.load_state_dict(checkpoint)
net.to("cpu")
net.eval()

# Preprocessing transformations
to_tensor = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])

def vis_parsing_maps(im, parsing_anno, stride):
    # Colors for all parts
    part_colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0],
                   [255, 0, 85], [255, 0, 170],
                   [0, 255, 0], [85, 255, 0], [170, 255, 0],
                   [0, 255, 85], [0, 255, 170],
                   [0, 0, 255], [85, 0, 255], [170, 0, 255],
                   [0, 85, 255], [0, 170, 255],
                   [255, 255, 0], [255, 255, 85], [255, 255, 170],
                   [255, 0, 255], [255, 85, 255], [255, 170, 255],
                   [0, 255, 255], [85, 255, 255], [170, 255, 255]]

    im = np.array(im)
    vis_im = im.copy().astype(np.uint8)
    vis_parsing_anno = parsing_anno.copy().astype(np.uint8)
    vis_parsing_anno = cv2.resize(vis_parsing_anno, None, fx=stride, fy=stride, interpolation=cv2.INTER_NEAREST)
    vis_parsing_anno_color = np.zeros((vis_parsing_anno.shape[0], vis_parsing_anno.shape[1], 3)) + 255

    num_of_class = np.max(vis_parsing_anno)
    for pi in range(1, num_of_class + 1):
        index = np.where(vis_parsing_anno == pi)
        vis_parsing_anno_color[index[0], index[1], :] = part_colors[pi]

    vis_parsing_anno_color = vis_parsing_anno_color.astype(np.uint8)
    vis_im = cv2.addWeighted(cv2.cvtColor(vis_im, cv2.COLOR_RGB2BGR), 0.4, vis_parsing_anno_color, 0.6, 0)

    # Encode the visualization into a byte array
    _, encoded_image = cv2.imencode('.jpg', vis_im)
    return encoded_image.tobytes()

def get_hair_color(image, parsing):
    hair_mask = (parsing == 17)
    hair_pixels = image[hair_mask]
    if hair_pixels.size == 0:
        raise ValueError("No hair pixels found in the mask.")
    return np.median(hair_pixels, axis=0).tolist()

def get_eye_color(image, parsing):
    eye_mask = (parsing == 5)
    eye_pixels = image[eye_mask]
    if eye_pixels.size == 0:
        raise ValueError("No eye pixels found in the mask.")
    return np.median(eye_pixels, axis=0).tolist()

def get_skin_color(image, parsing):
    neck_mask = (parsing == 15)
    neck_pixels = image[neck_mask]
    if neck_pixels.size == 0:
        skin_mask = (parsing == 0)
        skin_pixels = image[skin_mask]
        if skin_pixels.size == 0:
            raise ValueError("No skin pixels found in the mask.")
        return np.median(skin_pixels, axis=0).tolist()
    return np.median(neck_pixels, axis=0).tolist()

def get_undertones(image, parsing):
    neck_mask = (parsing == 2).astype(np.uint8) * 255
    neck_pixels = cv2.bitwise_and(image, image, mask=neck_mask)
    if neck_pixels.size == 0:
        skin_mask = (parsing == 0)
        skin_pixels = cv2.bitwise_and(image, image, mask=skin_mask.astype(np.uint8) * 255)
        if skin_pixels is None or skin_pixels.size == 0:
            raise ValueError("No skin pixels found in the mask.")
        return classify_tone(skin_pixels)
    return classify_tone(neck_pixels)

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Serverless function to process an uploaded image, extract features, and return results.
    """
    try:
        # Read and preprocess the image
        contents = await file.read()

        # Open with PIL for processing and resizing
        img = Image.open(contents).convert("RGB")
        image = img.resize((512, 512), Image.BILINEAR)
        image_np = np.array(image)  # Convert to NumPy array for further processing

        # Also prepare the image using cv2.imread-like functionality
        cv_image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        cv_image = cv2.resize(cv_image, (512, 512), interpolation=cv2.INTER_LINEAR)

        # Run the segmentation model
        img_tensor = to_tensor(image).unsqueeze(0)
        with torch.no_grad():
            out = net(img_tensor)[0]
        parsing = out.squeeze(0).cpu().numpy().argmax(0)

        # Extract features using the parsing map
        hair_color = get_hair_color(image_np, parsing)
        eye_color = get_eye_color(image_np, parsing)
        skin_color = get_skin_color(image_np, parsing)
        undertones = get_undertones(cv_image, parsing)  # Pass cv2.imread-like image

        # Visualize parsing map
        vis_image = vis_parsing_maps(image_np, parsing, stride=1)

        # Encode the visualized image as a Base64 string
        vis_image_base64 = base64.b64encode(vis_image).decode("utf-8")

        # Return results as JSON
        return {
            "hair_color": hair_color,
            "eye_color": eye_color,
            "skin_color": skin_color,
            "undertones": undertones,
            "visualized_image": vis_image_base64
        }
    except Exception as e:
        return {"error": str(e)}
