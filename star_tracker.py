"""
Filename: main.py
Author: Katie Jiang
Date: 2026-11-21
Description: Intended start up script. Captures jpg/pkl image every ~second until interrupted.
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

def set_img_quality(qlty = 90, compression = 1): # default values from PiCamera2
    """Set jpeg quality (0-95) and png compression level (0-9)
    Call before picam2.start()
    """
    if (qlty < 0 or qlty > 95):
        return
    if (compression > 9 or compression < 0):
        return
    picam2.options["quality"] = qlty
    picam2.options["compression_level"] = compression

def capture_jpeg(fname, request):
    """Save photo as jpeg/jpg"""
    metadata = request.get_metadata()
    img = request.make_image("main")
    img_path = filepath + "photos/" + fname + ".jpg"
    picam2.helpers.save(img, metadata, img_path)
    print("JPG Image Successfully Captured")

# Capture image as numpy array saved as pickle
def capture_pkl(fname, request):
    """Save photo as numpy array in txt file"""
    img_array = request.make_array("main")
    pickle_path = filepath + "photos/" + fname + ".pkl"
    with open(pickle_path, 'wb') as file:
        # pickle.dump(img_array, pickle_path) # Pickle with protocol 0
        pickle.dump(img_array, file, -1) # Pickle the list using the highest protocol available.
    print("Numpy Array Successfully Captured as Pickle")
    # TODO: Convert numpy array to jpeg to ensure they are the same photo

# ============================================================
# CONFIGURATION
# ============================================================

exposure_s = 1 # 1 second
exposure_us = exposure_s * 1_000_000
# HQ Camera Module does not support autofocus
# Attempting to set the af control will fail.
ctrls = {
    "AeEnable": False, # no autoexposure
    "AwbEnable": False, # no auto white balance
    "ExposureTime": exposure_us,
    "AnalogueGain": 1.0,
    # max + min time (us) that sensor can take to deliver a frame
    "FrameDurationLimits": (exposure_us + 1000, exposure_us + 1000),
    "NoiseReductionMode": 0, # draft.NoiseReductionModeEnum.Off
    "Sharpness": 0.0,
    # HDR mode is disabled by default
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
        # TODO: get fractional seconds
        curr = datetime.now().strftime("%Y-%m-%d %H%M%S")   # Grab datetime for file naming
        request = picam2.capture_request()
        capture_jpeg(str(curr), request)    # Capture image as jpg
        # capture_pkl(str(curr), request)     # Capture image as pickle
        request.release()
        time.sleep(exposure_s) # Interval
except KeyboardInterrupt:
    pass
