"""
6.1.1 Capturing Arrays

Combined with parts of hello-world.py
To cross-reference numpy array with jpg image
Outputs numpy array as pickle
"""

import sys
import pickle # want to dump numpy array as pickle
from picamera2 import Picamera2, Preview
import numpy as np
import time
from datetime import datetime

# Configure camera + preview
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
# Start camera
picam2.start()
time.sleep(2) # Preview delay

# Grab datetime for file naming
curr = datetime.now().strftime("%Y-%m-%d %H%M%S")
# Capture image as jpg
picam2.capture_file("photos/" + str(curr) + ".jpg") # Capture as jpg file
print("JPG Image Successfully Captured")
# Capture image as array to txt file
img_array = picam2.capture_array("main")
# print("Printing truncated numpy array...")
# print(img_array)
pickle_path = "photos/" + str(curr) + ".pkl"
with open(pickle_path, 'w') as file:
    # pickle.dump(img_array, pickle_path) # Pickle with protocol 0
    pickle.dump(img_array, file, -1) # Pickle the list using the highest protocol available.
print("Numpy Array Successfully Captured as Pickle")
