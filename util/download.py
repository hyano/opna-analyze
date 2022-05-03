import sys
import time
import serial

ser = serial.Serial("/dev/tty.usbserial-ABSCDZ0I", 19200, timeout=None)

while True:
    c = ser.read()
    print(c.decode(), end="")
