import sys
import time
import serial

ser = serial.Serial("/dev/tty.usbserial-ABSCDZ0I", 19200)

with open(sys.argv[1]) as f:
    for line in f:
        line = line.rstrip()
        print(line)
        ser.write((line+"\r").encode())
        time.sleep(0.1)
