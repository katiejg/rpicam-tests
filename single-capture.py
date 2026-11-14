#!/usr/bin/python3
"""
Filename: single-capture.py
Author: Katie Jiang
Date: 2026-10-31
Description: See "6.3. Capturing multiple images at once" in the Picamera2 module.
"""

import sys
import os
import pickle # want to dump numpy array as pickle
from picamera2 import Picamera2, Preview
import numpy as np
import time
from datetime import datetime

picam2 = Picamera2()
# TODO: Change the file path to where the photos directory is located on the system
# Use `realpath file` in terminal
filepath = '/home/farhorizons/Desktop/rpicam-tests/'

# Configuration
capture_config = picam2.create_still_configuration()
picam2.configure(capture_config)

# Capture image as numpy array saved as pickle
def to_pkl(img_array):
    """Save photo as numpy array in txt file"""
    # img_array = picam2.capture_array("main")
    # print("Printing truncated numpy array...")
    # print(img_array)
    pickle_path = filepath + "photos/" + fname + ".pkl"
    with open(pickle_path, 'wb') as file:
        # pickle.dump(img_array, pickle_path) # Pickle with protocol 0
        pickle.dump(img_array, file, -1) # Pickle the list using the highest protocol available.
    print("Numpy Array Successfully Captured as Pickle")

# Start camera
try:
    picam2.start()
    # curr = datetime.now().strftime("%Y-%m-%d %H%M%S")   # Grab datetime for file naming
    buffer = picam2.capture_buffer()
    metadata = picam2.capture_metadata()
    img_array = picam2.helpers.make_array()
    to_pkl(img_array)
    img = picam2.helpers.make_image(buffer, picam2.camera_configuration())
    picam2.helpers.save(img, metadata, "/photos/file.jpg")
