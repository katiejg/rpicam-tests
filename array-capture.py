#
# 6.1.1 Capturing Arrays
#
# Combined with parts of hello-world.py
# To cross-reference numpy array with jpg image

from picamera2 import Picamera2
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
print("JPG image captured")
# Capture image as array to txt file
img_array = picam2.capture_array("main")
txtfile_path = "photos/" + str(curr) + ".txt"
with open(txtfile_path, 'w') as file:
    file.write(img_array)
print("Numpy array captured")
