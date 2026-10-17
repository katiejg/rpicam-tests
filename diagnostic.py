import time
from datetime import datetime
from gpiozero import CPUTemperature

cpu = CPUTemperature()
folderpath = '/home/farhorizons/Desktop/rpicam-tests/'
curr = datetime.now().strftime("%Y-%m-%d %H%M%S")   # Grab datetime for file naming

filepath = folderpath + "logs/" + curr + ".csv"
with open("cpu_temperature_log.csv", "w") as f:
    f.write("Timestamp,Temperature_C\n")
    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        temp = cpu.temperature
        f.write(f"{timestamp},{temp:.2f}\n")
        f.flush()
        time.sleep(2)  # log every 10 seconds
