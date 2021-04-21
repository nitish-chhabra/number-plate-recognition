from matplotlib import pyplot as plt
import numpy as np

import cv2
import easyocr
import imutils

from . import functions

input_type = "Image"  # Image / Video / Camera
use_gpu = "False"     # True / False
data_path = "./dataset/"        # Only accessed when input_type is in -> Image, Camera

assert input_type.lower() in ["image", "video", "camera"], "Please give a valid input type"

if input_type == "Image":
    img = cv2.imread(data_path)
else:
    pass