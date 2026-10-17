import time
import subprocess
from datetime import datetime
from gpiozero import CPUTemperature

cpu = CPUTemperature()
FOLDER_PATH = '/home/farhorizons/Desktop/rpicam-tests/'
curr = datetime.now().strftime("%Y-%m-%d %H%M%S")   # Grab datetime for file naming
filepath = FOLDER_PATH + "logs/" + curr + ".csv"

def vcgencmd(*args):
    """Run vcgencmd and return stdout, or None on failure."""
    try:
        out = subprocess.run(
            ["vcgencmd", *args], capture_output=True, text=True, timeout=5, check=True
        )
        return out.stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        return None

with open("cpu_temperature_log.csv", "w") as f:
    f.write("Timestamp,Temperature_C\n")
    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        temp = cpu.temperature
        f.write(f"{timestamp},{temp:.2f}\n")
        f.flush()
        time.sleep(2)  # log every 10 seconds
