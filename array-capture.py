#
# 6.1.1 Capturing Arrays
#

from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.start()

time.sleep(1)
array = picam2.capture_array("main")
print(array)
