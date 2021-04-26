import time
import cv2
import sys

from . import functions as internal_functions

input_type = "Image"  # Image / Video / Camera
extract_number_plate = 1 # 1 / 0, 1 means extract and 0 means skip
data_path = "./dataset/JPEGImages/car_25.jpg"        # Only accessed when input_type is in -> Image, Camera
output_resolution_height = 1280
output_resolution_width = 800
counter = 0

assert input_type.lower() in ["image", "video", "camera"], "Please give a valid input type"


if '__name__' == '__main__':


    if input_type.lower() == "image":
        frame = cv2.imread(data_path)
        cropped_frame, plate_location = internal_functions.extract_contours(frame)
        if extract_number_plate:
            internal_functions.read_number_plate(cropped_frame)
        else:
            pass

    else:
        if input_type.lower() == "camera":
            captured_video = cv2.VideoCapture(0)
        elif input_type.lower() == "video" and len(data_path):
            captured_video = cv2.VideoCapture(data_path)
        else:
            print("Wrong input type provided, exiting")
            sys.exit()

        while True:
            a = time.time_ns()
            was_the_frame_read, frame = captured_video.read()

            if was_the_frame_read:
                cropped_frame, plate_location = internal_functions.extract_contours(frame)
            if extract_number_plate:
                internal_functions.read_number_plate(cropped_frame)
            else:
                pass



            if counter:
                b = time.time_ns()
                try:
                    fps = round(1/((b-a)/ (10 ** 9)),1)
                except:
                    fps = "Unlimited"

            cv2.putText(img=frame, text=str(fps), org=(250, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,color=(0, 255, 255), thickness=2, lineType=cv2.LINE_4)

            k = cv2.waitKey(1)
            if k == ord('q'):
                break
        
        captured_video.release()
        cv2.destroyAllWindows()

    img = cv2.imread(data_path)