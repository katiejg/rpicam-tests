"""
Filename: cam-config.py
Author: Katie Jiang
Date: 2026-10-23
Description: Playing with camera configuration
"""

from picamera2 import Picamera2
import time
from datetime import datetime

picam2 = Picamera2()

exposure_us = 10_000_000  # 20 seconds
ctrl_1 = {
    "AeEnable": False,
    "AwbEnable": False,
    "ExposureTime": exposure_us,
    "AnalogueGain": 1.0,
    "FrameDurationLimits": (exposure_us + 1000, exposure_us + 1000),
    "NoiseReductionMode": 0,
    "Sharpness": 0.0,
}
ctrls = ctrl_1; # ctrls are what is actually configured!

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

camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
set_img_quality(95, 0) # highest quality, no compression
# Call controls here!
picam2.set_controls(ctrls);
# print(picam2.camera_properties);

try:
    picam2.start()
    curr = datetime.now().strftime("%Y-%m-%d_%H%M%S")   # Grab datetime for file naming
    time.sleep(1 + exposure_us/1000000) # in seconds
    picam2.capture_file("photos/" + str(curr) + ".jpg")
    time.sleep(1)
except KeyboardInterrupt:
    pass
