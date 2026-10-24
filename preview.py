"""
Filename: preview.py
Author: Katie Jiang
Date: 2026-10-23
Description: Indefinite preview window
"""

from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)

try:
    picam2.start()
    while True:
        time.sleep(100) # Preview delay
except KeyboardInterrupt:
    pass
