import cv2
import numpy as np

def convert_image(img_data):
    # This looks like an OK way to load images
    nparr = np.frombuffer(img_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(img_np , cv2.COLOR_BGR2RGB)
    return imageRGB
