#!/usr/bin/env python3
# Modified from:
# https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_1-Wire_DS18B20_Sensor

import os
import glob
import time

import argparse
import csv
import re
import subprocess
from datetime import datetime
from pathlib import Path

folderpath = '/home/farhorizons/Desktop/rpicam-tests/'

# These tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_rom():
    name_file=device_folder+'/name'
    f = open(name_file,'r')
    return f.readline()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

curr = datetime.now().strftime("%Y-%m-%d_%H%M%S")   # Grab datetime for file naming
filepath = folderpath + "logs/ds18b20_" + curr + ".csv"
with open(filepath, "w") as f:
    f.write("Timestamp,ROM,Temperature_C,Temperature_F\n")
    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        rom = read_rom()
        temp_c, temp_f = read_temp()
        f.write(f"{timestamp},{rom},{temp_c:.3f},{temp_f:.3f}\n")
        f.flush()
        time.sleep(2)  # log every 2 seconds
