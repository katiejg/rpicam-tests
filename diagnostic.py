#!/usr/bin/env python3
# ===============================
# CLAUDE-GENERATED CODE
# ===============================
"""Raspberry Pi 5 diagnostic monitor: temperature, voltages, throttle state.
"""

import argparse
import csv
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

folderpath = '/home/farhorizons/Desktop/rpicam-tests/'
THERMAL_PATH = Path("/sys/class/thermal/thermal_zone0/temp")

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
filepath = "logs/" + curr + ".csv"
with open(filepath, "w") as f:
    f.write("Timestamp,Temperature_C,Core_V,Ext5V_V,Throttle\n")
    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        temp = read_temp_c()
        core = read_core_volts()
        rails = read_pmic_rails()
        ext5v = rails.get("EXT5V_V")
        throttle = read_throttle_state()
        f.write(f"{timestamp},{temp:.2f},{core:.2f},{ext5v:.2f},{throttle}\n")
        f.flush()
        time.sleep(5)  # log every 2 seconds
