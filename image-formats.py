"""

"""

import sys
from picamera2 import Picamera2, Preview
import numpy as np
import time
from datetime import datetime

picam2 = Picamera2()

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def capture_jpeg(fname):
    """Save photo as jpeg/jpg"""
    picam2.capture_file("photos/" + fname + ".jpg")
    print("JPG Image Successfully Captured")

def capture_png(fname):
    """Save photo as png"""
    picam2.capture_file("photos/" + fname + ".png")
    print("PNG Image Successfully Captured")

# Capture image as numpy array saved to
def capture_np(fname):
    """Save photo as numpy array in txt file"""
    img_array = picam2.capture_array("main")
    print("Printing truncated numpy array...")
    print(img_array)
    txtfile_path = "photos/" + fname + ".txt"
    with open(txtfile_path, 'w') as file:
        file.write(np.array2string(img_array, separator=',', threshold=sys.maxsize))
    print("Numpy Array Successfully Captured")

# Configure camera + preview
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)

# Start camera
picam2.start()
time.sleep(2) # Preview delay

# Grab datetime for file naming
curr = datetime.now().strftime("%Y-%m-%d %H%M%S")
# Capture image as jpg
capture_jpeg(str(curr));
# Capture image as array to txt file
capture_np(str(curr));
