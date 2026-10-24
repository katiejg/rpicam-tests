"""
Filename: image-formats.py
Author: Katie Jiang
Date: 2026-10-17
Description: Playing with image formats in the picamera2 lib, spinning off of `array-capture.py`
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

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def preview_qtgl():
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)

def set_img_quality(qlty = 90, compression = 1):
    """Set jpeg quality (0-95) and png compression level (0-9)
    Call before picam2.start()
    """
    # Some data validation...
    if (qlty < 0 or qlty > 95):
        return
    if (compression > 9 or compression < 0):
        return
    picam2.options["quality"] = qlty
    picam2.options["compression_level"] = compression

def capture_jpeg(fname):
    """Save photo as jpeg/jpg"""
    picam2.capture_file(filepath + "photos/" + fname + ".jpg")
    print("JPG Image Successfully Captured")

def capture_png(fname):
    """Save photo as png"""
    picam2.capture_file(filepath + "photos/" + fname + ".png")
    print("PNG Image Successfully Captured")

# Capture image as numpy array saved to text
def capture_np(fname):
    """Save photo as numpy array in txt file"""
    img_array = picam2.capture_array("main")
    print("Printing truncated numpy array...")
    print(img_array)
    txtfile_path = filepath + "photos/" + fname + ".txt"
    with open(txtfile_path, 'w') as file:
        file.write(np.array2string(img_array, separator=',', threshold=sys.maxsize))
    print("Numpy Array Successfully Captured")

# Capture image as numpy array saved as pickle
def capture_pkl(fname):
    """Save photo as numpy array in txt file"""
    img_array = picam2.capture_array("main")
    # print("Printing truncated numpy array...")
    # print(img_array)
    pickle_path = filepath + "photos/" + fname + ".pkl"
    with open(pickle_path, 'wb') as file:
        # pickle.dump(img_array, pickle_path) # Pickle with protocol 0
        pickle.dump(img_array, file, -1) # Pickle the list using the highest protocol available.
    print("Numpy Array Successfully Captured as Pickle")


# Configure camera + preview
# preview_qtgl() # Comment to turn off preview
set_img_quality(95, 0) # highest quality, no compression

# Start camera
try:
    picam2.start()
    while True:
        time.sleep(1) # Preview delay
        curr = datetime.now().strftime("%Y-%m-%d %H%M%S")   # Grab datetime for file naming
        capture_jpeg(str(curr));    # Capture image as jpg
        capture_png(str(curr));     # Capture image as png
        # capture_np(str(curr));      # Capture image as array to txt file
        # capture_pkl(str(curr));
        time.sleep(2) # Interval
except KeyboardInterrupt:
    pass
