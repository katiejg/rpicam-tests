#!/usr/bin/env python3
# ===============================
# CLAUDE-GENERATED CODE
# In addition to modifications to:
# https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_1-Wire_DS18B20_Sensor
# ===============================
"""Raspberry Pi 5 diagnostic monitor: temperature, voltages, throttle state.
"""
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
THERMAL_PATH = Path("/sys/class/thermal/thermal_zone0/temp")

# These tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folders = [glob.glob(base_dir + '28*')[0], glob.glob(base_dir + '28*')[1]]
device_files = [glob.glob(base_dir + '28*')[0] + '/w1_slave', glob.glob(base_dir + '28*')[1] + '/w1_slave']

def read_rom(index):
    name_file=device_folders[index]+'/name'
    f = open(name_file,'r')
    return f.readline()

def read_temp_raw(index):
    f = open(device_files[index], 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(index):
    lines = read_temp_raw(index)
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(index)
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Bit meanings for `vcgencmd get_throttled`
THROTTLE_FLAGS = {
    0: "under-voltage now",
    1: "ARM freq capped now",
    2: "throttled now",
    3: "soft temp limit now",
    16: "under-voltage occurred",
    17: "ARM freq capping occurred",
    18: "throttling occurred",
    19: "soft temp limit occurred",
}

def vcgencmd(*args):
    """Run vcgencmd and return stdout, or None on failure."""
    try:
        out = subprocess.run(
            ["vcgencmd", *args], capture_output=True, text=True, timeout=5, check=True
        )
        return out.stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        return None

def read_temp_c():
    """CPU/SoC temperature in Celsius (sysfs, falls back to vcgencmd)."""
    try:
        return int(THERMAL_PATH.read_text()) / 1000.0
    except (OSError, ValueError):
        out = vcgencmd("measure_temp")  # e.g. temp=48.7'C
        m = re.search(r"temp=([\d.]+)", out or "")
        return float(m.group(1)) if m else None

def read_core_volts():
    """SoC core voltage (the Pi's internal voltage) in volts."""
    out = vcgencmd("measure_volts", "core")  # e.g. volt=0.8800V
    m = re.search(r"volt=([\d.]+)V", out or "")
    return float(m.group(1)) if m else None


def read_pmic_rails():
    """Return a dict of PMIC voltage rails, e.g. {'EXT5V_V': 4.95, ...}.

    EXT5V_V is the 5V input supply as seen by the PMIC - the best indicator
    of a weak power adapter or cable.
    """
    out = vcgencmd("pmic_read_adc")
    rails = {}
    for name, val in re.findall(r"(\w+_V)\s+volt\(\d+\)=([\d.]+)V", out or ""):
        rails[name] = float(val)
    return rails

def read_throttle_state():
    """Decode get_throttled into a list of active flag descriptions."""
    out = vcgencmd("get_throttled")  # e.g. throttled=0x50005
    m = re.search(r"0x([0-9a-fA-F]+)", out or "")
    if not m:
        return None
    value = int(m.group(1), 16)
    return [desc for bit, desc in THROTTLE_FLAGS.items() if value & (1 << bit)]

def fmt(value, spec):
    return format(value, spec) if value is not None else "n/a"

curr = datetime.now().strftime("%Y-%m-%d_%H%M%S")   # Grab datetime for file naming
filepath = folderpath + "logs/" + curr + ".csv"
with open(filepath, "w") as f:
    f.write("Timestamp,Temperature_C,Core_V,Ext5V_V,Throttle,ROM[0],Temperature_C[0],Temperature_F[0],ROM[1],Temperature_C[1],Temperature_F[1]\n")
    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        temp = read_temp_c()
        core = read_core_volts()
        rails = read_pmic_rails()
        ext5v = rails.get("EXT5V_V")
        throttle = read_throttle_state()
        rom0 = read_rom(0)
        temp_c0, temp_f0 = read_temp(0)
        rom1 = read_rom(1)
        temp_c1, temp_f1 = read_temp(1)
        f.write(f"{timestamp},{temp:.2f},{core:.2f},{ext5v:.2f},{throttle},{rom0},{temp_c0:.3f},{temp_f0:.3f},{rom1},{temp_c1:.3f},{temp_f1:.3f}\n")
        f.flush()
        time.sleep(2)  # log every 2 seconds
