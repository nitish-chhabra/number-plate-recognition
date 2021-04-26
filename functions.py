from matplotlib import pyplot as plt
import numpy as np

import cv2
import easyocr
import imutils


def extract_contours(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None   # Only for showing the small image of exactly the number plate
    for contour in contours:
        plate_location = cv2.approxPolyDP(contour, 10, True)
        if len(plate_location) == 4:
            location = plate_location
            break

    mask = np.zeros(gray.shape, np.uint8)
    # new_image = cv2.drawContours(mask, [location], 0,255, -1)
    # new_image = cv2.bitwise_and(img, img, mask=mask)
    # plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)) # Shows the cropped image of number plate

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    return cropped_image, plate_location

def read_number_plate(cropped_frame, plate_location):
    reader = easyocr.Reader(['en'])
    number_plate = reader.readtext(cropped_frame)
    print(number_plate)

    final_frame_with_plate = cv2.putText(cropped_frame, text=number_plate[0][-2], org=(plate_location[0][0][0], plate_location[1][0][1]+60), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,255,0), thickness=3, lineType=cv2.LINE_AA)
    final_frame_with_plate = cv2.rectangle(cropped_frame, tuple(plate_location[0][0]), tuple(plate_location[2][0]), (0,255,0),3)
    # plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
    return final_frame_with_plate
