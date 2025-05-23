import requests
import json

def test_classify_season_api():
    # URL of your local API
    url = "http://127.0.0.1:8000/api/classify_season"

    # Path to the test image
    test_image_path = "sample_inputs/valid_face_2.png"
    

    # Read the test image as binary
    with open(test_image_path, "rb") as file:
        files = {"file": file}
        
        # Send POST request to the API
        response = requests.post(url, files=files)

    # Print the response from the API
    print("Status Code:", response.status_code)
    print("Response Text:", response.text) 

def test_classify_color_api():
    # URL of your local API
    url = "http://127.0.0.1:8000/api/classify_color"

    # Path to the test image
    test_image_path = "sample_inputs/shirt.jpg"
    

    # Read the test image as binary
    with open(test_image_path, "rb") as file:
        files = {"file": file}
        
        # Send POST request to the API
        response = requests.post(url, data={"season_dict": '{"season": "Bright Spring"}'}, files=files)
    print(response)

    # Print the response from the API
    print("Status Code:", response.status_code)
    print("Response Text:", response.text) 

if __name__ == "__main__":
    test_classify_color_api()
