import sys
import re
import time
import serial

ser = serial.Serial("/dev/tty.usbserial-ABSCDZ0I", 19200)

with open(sys.argv[1]) as f:
    for line in f:
        line = line.rstrip()
        if not re.match(r'^\d+', line):
            next

        ser.write((line+"\r").encode())

        while True:
            c = ser.read(1).decode()
            if c == "@":
                break
            elif c == "\r":
                print("")
            elif c == "\n":
                pass
            else:
                print(c, end="")
