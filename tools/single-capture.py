#!/usr/bin/python3
"""
Filename: single-capture.py
Author: Katie Jiang
Date: 2026-11-14
Description: Captures and saves one frame as both a jpg and pkl. See "6.3. Capturing multiple images at once" in the Picamera2 module.
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
def set_img_quality(qlty = 90, compression = 1):
    """Set jpeg quality (0-95) and png compression level (0-9)
    Call before picam2.start()
    """
    if (qlty < 0 or qlty > 95):
        return
    if (compression > 9 or compression < 0):
        return
    picam2.options["quality"] = qlty
    picam2.options["compression_level"] = compression

def to_pkl(fname, img_array):
    """Capture image as numpy array saved as pickle"""
    # img_array = picam2.capture_array("main")
    # print("Printing truncated numpy array...")
    # print(img_array)
    pickle_path = filepath + "photos/" + fname + ".pkl"
    with open(pickle_path, 'wb') as file:
        # pickle.dump(img_array, pickle_path) # Pickle with protocol 0
        pickle.dump(img_array, file, -1) # Pickle the list using the highest protocol available.
    print("Numpy Array Successfully Captured as Pickle")

# Capture image as numpy array saved as pickle
def to_jpg(fname, img, metadata):
    """Save photo as jpg"""
    # img_array = picam2.capture_array("main")
    # print("Printing truncated numpy array...")
    # print(img_array)
    img_path = filepath + "photos/" + fname + ".jpg"
    picam2.helpers.save(img, metadata, img_path)
    print("Frame Successfully Saved as JPG")

# ==================================================
# CONFIGURATION
# ==================================================
exposure_s = 1 # 1 second
exposure_us = exposure_s * 1_000_000
ctrls = {
    "AeEnable": False, # no autoexposure
    "AwbEnable": False, # no auto white balance
    "ExposureTime": exposure_us,
    "AnalogueGain": 1.0,
    # min + max time (us) that sensor can take to deliver a frame
    "FrameDurationLimits": (exposure_us + 1000, exposure_us + 1000),
    "NoiseReductionMode": 0,
    "Sharpness": 0.0,
}

camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
set_img_quality(95, 0) # highest quality, no compression
picam2.set_controls(ctrls);

# ==================================================
# MAIN
# ==================================================
# Start camera
try:
    picam2.start()
    curr = datetime.now().strftime("%Y-%m-%d %H%M%S")   # Grab datetime for file naming

    request = picam2.capture_request()
    metadata = request.get_metadata()
    img_array = request.make_array("main")
    to_pkl(str(curr), img_array)
    img = request.make_image("main")
    to_jpg(str(curr),img, metadata)
except KeyboardInterrupt:
    pass
