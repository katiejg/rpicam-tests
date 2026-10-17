import time
from gpiozero import CPUTemperature

cpu = CPUTemperature()

with open("cpu_temperature_log.csv", "w") as f:
    f.write("Timestamp,Temperature_C\n")
    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        temp = cpu.temperature
        f.write(f"{timestamp},{temp:.2f}\n")
        f.flush()
        time.sleep(10)  # log every 10 seconds
