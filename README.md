Experiments with a Raspberry Pi 5 and High Quality Camera (Sony IMX477) module.

## Running a script
This repository should be in the Desktop of the Raspberry Pi. In terminal, `cd` to the repository. Once you are in the folder, you can simply enter `python script_name.py` to run the script.

## Operating the Raspberry Pi
1. Power the Raspberry Pi on (indicated by the green light on the board)
2. It automatically runs the [star_tracker.py](https://github.com/katiejg/rpicam-tests/blob/experimental/star_tracker.py) script at start using the [autostart](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup/all#method-2-autostart) method
3. To stop this program, you need to log into the GUI of the Pi. There should be a terminal open once you log in. Press Ctrl+C while in the terminal too interrupt the program.

## Logging into the Raspberry Pi
### Connect display and input devices
The easiest way to connect to the Pi is to use USB cables and an HDMI cable and plug in a monitor, a mouse, and keyboard. Then, you simply log in like a normal computer.
### Remote Access
[Here is a full reference](https://www.raspberrypi.com/documentation/computers/remote-access.html#introduction-to-remote-access) for how to access the Pi remotely. This requires the Raspberry Pi and your own laptop to be on the same network. The Raspberry I will explain each briefly below:
**SSH**
You can log into the Pi from your own laptop by entering `ssh farhorizons@pi-ip-address` into a terminal. This will give you terminal access to the Pi, but does not have a GUI.
**TigerVNC**
Requires installation of TigerVNC on your own laptop and allows you to access the GUI of the Pi.

## References
- [Picamera2 Library Manual](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [HQ Camera Documentation](https://www.raspberrypi.com/documentation/accessories/camera.html#hq-camera)
- [Camera Software Documentation](https://www.raspberrypi.com/documentation/computers/camera_software.html)
