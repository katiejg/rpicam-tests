"""
Filename: main.py
Author: Katie Jiang
Date: 2026-10-24
Description: Intended start up script. Captures jpg/png/pkl image every ~3 seconds until interrupted.
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

# ============================================================
# HELPER FUNCTIONS
# ============================================================

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

def capture_jpeg(fname):
    """Save photo as jpeg/jpg"""
    picam2.capture_file(filepath + "photos/" + fname + ".jpg")
    print("JPG Image Successfully Captured")

def capture_png(fname):
    """Save photo as png"""
    picam2.capture_file(filepath + "photos/" + fname + ".png")
    print("PNG Image Successfully Captured")

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

# ============================================================
# CONFIGURATION
# ============================================================

exposure_s = 1 # 5 seconds
exposure_us = exposure_s * 1_000_000
ctrls = {
    "AeEnable": False, # no autoexposure
    "AwbEnable": False, # no auto white balance
    "ExposureTime": exposure_us,
    "AnalogueGain": 1.0,
    "FrameDurationLimits": (exposure_us + 1000, exposure_us + 1000),
    "NoiseReductionMode": 0,
    "Sharpness": 0.0,
}

camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
set_img_quality(95, 0) # highest quality, no compression
picam2.set_controls(ctrls);

# ============================================================
# MAIN LOOP
# ============================================================

# Start camera
try:
    picam2.start()
    while True:
        time.sleep(1) # Preview delay
        curr = datetime.now().strftime("%Y-%m-%d %H%M%S")   # Grab datetime for file naming
        capture_jpeg(str(curr))    # Capture image as jpg
        capture_png(str(curr))     # Capture image as png
        capture_pkl(str(curr))     # Capture image as pickle
        # time.sleep(exposure_s) # Interval
except KeyboardInterrupt:
    pass
