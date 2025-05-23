#!/usr/bin/python
# -*- encoding: utf-8 -*-

from logger import setup_logger
from model import BiSeNet
from scipy.stats import mode

import torch

import os
import os.path as osp
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import cv2
from UnderToneAnalysis import classify_tone


def vis_parsing_maps(im, parsing_anno, stride, save_im=False, save_path='vis_results/parsing_map_on_im.jpg'):
    # Colors for all 20 parts of the face we segment
    part_colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0],
                   [255, 0, 85], [255, 0, 170],
                   [0, 255, 0], [85, 255, 0], [170, 255, 0],
                   [0, 255, 85], [0, 255, 170],
                   [0, 0, 255], [85, 0, 255], [170, 0, 255],
                   [0, 85, 255], [0, 170, 255],
                   [255, 255, 0], [255, 255, 85], [255, 255, 170],
                   [255, 0, 255], [255, 85, 255], [255, 170, 255],
                   [0, 255, 255], [85, 255, 255], [170, 255, 255]]
    # mask dictionary: 0 = background, 1 = skin, 2 = r-eyebrow, 3 = l-eyebrow, 4 = r-eye, 5 = l-eye,  6-?, 7=l-ear, 8=?
    # 10 = nose, 12 = upper lip, 13=bottom lip

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
    # print(vis_parsing_anno_color.shape, vis_im.shape)
    vis_im = cv2.addWeighted(cv2.cvtColor(vis_im, cv2.COLOR_RGB2BGR), 0.4, vis_parsing_anno_color, 0.6, 0)

    # Save result or not
    if save_im:
        cv2.imwrite(save_path[:-4] +'.png', vis_parsing_anno)
        cv2.imwrite(save_path, vis_im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    # return vis_im

def get_hair_color(image, parsing):
    # expects an opened image
    # returns the median color of the hair
    hair_mask = (parsing == 17)
    
    hair_pixels = image[hair_mask]  # shape [num_hair_pixels, 3]
    
    if hair_pixels.size == 0:
        assert False, "No hair pixels found in the mask."
    else:
        # Compute the median color
        median_color = np.median(hair_pixels, axis=0)  # [R, G, B]
        return median_color
    
def get_eye_color(image, parsing):
    # expects an opened image
    # returns the median color of the eye
    eye_mask = (parsing == 5)
    eye_pixels = image[eye_mask]  
    
    if eye_pixels.size == 0:
        assert False, "No hair pixels found in the mask."
    else:
        # Compute the median color
        median_color = np.median(eye_pixels, axis=0)  # [R, G, B]
        return median_color
    
def get_skin_color(image, parsing):
    # expects an opened image
    # returns the median color of the hair
    neck_mask = (parsing == 14)
    neck_pixels = image[neck_mask] 
    
    if neck_pixels.size == 0:
        #TODO: if person has beard, this is a problem
        skin_mask = (parsing == 0)
        skin_pixels = image[skin_mask]
        if skin_pixels.size == 0:
            assert False, "No skin pixels found in the mask."
        else:
            # Compute the median color
            median_color = np.median(skin_pixels, axis=0)
            return median_color
    else:
        # Compute the median color
        median_color = np.median(neck_pixels, axis=0)  # [R, G, B]
        return median_color

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

            # Display the skin-masked image (optional)
            cv2.imshow("Skin Masked Image", skin_masked_image_bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Compute the tone using the skin mask
            tone = classify_tone(skin_masked_image_bgr)
            return tone
    else:
        # Create a masked image for the neck
        masked_image = np.zeros_like(image)  # Create a black image
        masked_image[neck_mask] = image[neck_mask]  # Apply the masked pixels
        masked_image_bgr = cv2.cvtColor(masked_image, cv2.COLOR_RGB2BGR)

        # Display the neck-masked image (optional)
        cv2.imshow("Neck Masked Image", masked_image_bgr)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Compute the tone using the neck mask
        tone = classify_tone(masked_image_bgr)
        return tone

def evaluate(respth='./res/test_res', dspth='./data', cp='model_final_diss.pth'):
    
    if not os.path.exists(respth):
        os.makedirs(respth)

    n_classes = 19
    net = BiSeNet(n_classes=n_classes)
    # net.cuda()
    net.to("cpu")
    save_pth = osp.join('res/cp', cp)
    # net.load_state_dict(torch.load(save_pth))
    checkpoint = torch.load(save_pth, map_location=torch.device('cpu'), weights_only=True)
    net.load_state_dict(checkpoint)

    net.eval()

    to_tensor = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    with torch.no_grad():
        for image_path in os.listdir(dspth):
            img = Image.open(osp.join(dspth, image_path)).convert("RGB")
            image = img.resize((512, 512), Image.BILINEAR)
            CVimage = cv2.imread(osp.join(dspth, image_path))
            CVimage = cv2.resize(CVimage, (512, 512), interpolation=cv2.INTER_LINEAR)
            # print(img.shape)
            # print("\n\n\n\n\n")
            img = to_tensor(image)
            img = torch.unsqueeze(img, 0)
            # img = img.cuda()
            out = net(img)[0]
            parsing = out.squeeze(0).cpu().numpy().argmax(0)
            # print(parsing)
            # print(np.unique(parsing))
            np_image = np.array(image)  # shape (512, 512, 3)
            print("Image:", image_path)
            print("Hair Color:", get_hair_color(np_image, parsing))
            print("Eye Color:", get_eye_color(np_image, parsing)) 
            print("Skin Color:", get_skin_color(np_image, parsing))
            print("Undertones:", get_undertones(np_image, parsing))

            vis_parsing_maps(image, parsing, stride=1, save_im=True, save_path=osp.join(respth, image_path))
            


if __name__ == "__main__":
    evaluate(dspth='../photos/faces', cp='79999_iter.pth')


