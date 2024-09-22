# -*- coding: utf-8 -*-
"""
Created on Fri May  3 15:33:30 2024

@author: user
"""

import cv2
import os
from pypylon import pylon
from ultralytics import YOLO

# Load YOLOv8 model
#model = YOLO("./best.pt")  # Replace with your model path

# Setup and connect to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# Create the folder on the desktop to save images in 'correct_filters'
save_folder = os.path.join(os.path.expanduser("~"), 'Desktop', 'yolov8pictures')
os.makedirs(save_folder, exist_ok=True)

def nothing(x):
    pass

# Create trackbars for confidence and IoU
cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Confidence', 'Camera Feed', 50, 100, nothing)
cv2.createTrackbar('IoU', 'Camera Feed', 50, 100, nothing)

image_count = 0

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Convert the image to OpenCV format
        image = converter.Convert(grabResult)
        #frame = image.GetArray()

        # Get values from trackbars
        #conf = cv2.getTrackbarPos('Confidence', 'Camera Feed') / 100.0
        #iou = cv2.getTrackbarPos('IoU', 'Camera Feed') / 100.0

        # Perform object detection
        #results = model(frame, conf=conf, iou=iou)
        #annotated_frame = results[0].plot()  # Assuming plot() returns the annotated frame

        # Adjust the window size to match the frame size
        #cv2.resizeWindow('Camera Feed', annotated_frame.shape[1], annotated_frame.shape[0])

        # Display the image with detections
        #cv2.imshow('Camera Feed', annotated_frame)

        key = cv2.waitKey(1) & 0xFF
        # Capture and save an image upon pressing 's'
        if key == ord('s'):
            image_count += 1
            image_path = os.path.join(save_folder, f'image_{image_count}.png')
            cv2.imwrite(image_path, image)
            print(f"Saved image: {image_path}")

        # Exit the loop if the user closes the window
        if key == 27:  # 27 is the escape key
            break

    grabResult.Release()

# Cleanup
camera.StopGrabbing()
cv2.destroyAllWindows()