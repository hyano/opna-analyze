import sys
import re
import time
import random
import serial

class RsOPNA:
    def __init__(self):
        pass

    def open(self):
        self.ser = serial.Serial("/dev/tty.usbserial-ABSCDZ0I", 19200)

    def wait(self):
        while True:
            c = self.ser.read(1).decode()
            if c == "@":
                break
            elif c == "\r":
                print("")
            elif c == "\n":
                pass
            else:
                print(c, end="")

    def send(self, cmd):
        self.ser.write(cmd.encode())
        self.wait()
        self

    def out(self, reg, data):
        cmd = "1,{:02X},{:02X}\r".format(reg, data)
        self.send(cmd)
        return self

    def inp(self, reg):
        cmd = "2,{:02X}\r".format(reg)
        self.sned(cmd)
        return self

    def stat(self):
        cmd = "3\r"
        self.send(cmd)
        return self

    def nl(self):
        cmd = "4\r"
        self.send(cmd)
        return self

    def msg(self, msg):
        cmd = "5,{:s}\r".format(msg)
        self.send(cmd)
        return self

    def out0(self, reg, data):
        cmd = "6,{:02X},{:02X}\r".format(reg, data)
        self.send(cmd)
        return self

    def inp0(self, reg):
        cmd = "7,{:02X}\r".format(reg)
        self.sned(cmd)
        return self

    def stat0(self):
        cmd = "8\r"
        self.send(cmd)
        return self

    def poll_stat(self, wt):
        cmd = "9\r"
        self.ser.write(cmd.encode())
        time.sleep(wt)
        self.send("\r")
        return self

    def mwr(self, data, count):
        cmd = "10,{:02X},{:d}\r".format(data, count)
        self.send(cmd)
        return self

    def mrd(self, count):
        cmd = "11,{:d}\r".format(count)
        self.send(cmd)
        return self

    def reset(self):
        self.out(0x00, 0x01).out(0x00, 0x00).nl()

    def seq_mem_limit(self, adr):
        self.out(0x0c, adr & 0xff).out(0x0d, (adr >> 8) & 0xff)

    def seq_mem_write(self, start, stop, data, count, msg):
        self.msg(msg)
        self.out(0x10, 0x00).out(0x10, 0x80)
        self.out(0x00, 0x60).out(0x01, 0x02)
        self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
        self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
        self.nl()
        self.mwr(data, count).nl()
        self.out(0x00, 0x00).out(0x10, 0x80).nl()

    def seq_mem_read(self, start, stop, count, msg):
        self.msg(msg)
        self.out(0x10, 0x00).out(0x10, 0x80)
        self.out(0x00, 0x20).out(0x01, 0x02)
        self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
        self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
        self.nl()
        self.mrd(count).nl()
        self.out(0x00, 0x00).out(0x10, 0x80).nl()

    def seq_mem_fill(self, start, stop, data, count, msg):
        self.msg(msg)
        self.out(0x10, 0x00).out(0x10, 0x80)
        self.out(0x00, 0x60).out(0x01, 0x02)
        self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
        self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
        self.nl()
        for i in range(count):
            if (i % 16) == 0:
                print("\n{:05x} ".format(i), end="")
            self.out(0x08, data)
        self.out(0x00, 0x00).out(0x10, 0x80).nl()

    def seq_mem_fill_pat(self, start, stop, pat, count, msg):
        self.msg(msg)
        self.out(0x10, 0x00).out(0x10, 0x80)
        self.out(0x00, 0x60).out(0x01, 0x02)
        self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
        self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
        self.nl()
        l = len(pat)
        for i in range(count):
            if (i % 16) == 0:
                print("\n{:05x} ".format(i), end="")
            self.out(0x08, pat[i % l])
        self.out(0x00, 0x00).out(0x10, 0x80).nl()

    def seq_mem_fill_random(self, start, stop, count, msg):
        self.msg(msg)
        self.out(0x10, 0x00).out(0x10, 0x80)
        self.out(0x00, 0x60).out(0x01, 0x02)
        self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
        self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
        self.nl()
        for i in range(count):
            if (i % 16) == 0:
                print("\n{:05x} ".format(i), end="")
            self.out(0x08, random.randint(0x00, 0xff))
        self.out(0x00, 0x00).out(0x10, 0x80).nl()

    def seq_play(self, start, stop, deltan, volume, repeat, msg):
        self.msg(msg)
        self.out(0x10, 0x00).out(0x10, 0x80)
        self.out(0x00, 0x20)
        self.out(0x01, 0xc2)
        self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
        self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
        self.out(0x09, deltan & 0xff).out(0x0a, (deltan >> 8) & 0xff)
        self.out(0x0b, volume)
        if repeat:
            self.out(0x00, 0xb0)
        else:
            self.out(0x00, 0xa0)
        self.nl()

    def seq_stop(self, msg):
        self.msg(msg)
        self.out(0x00, 0xa1).poll_stat(0.1)
        self.out(0x00, 0x00).poll_stat(0.1).out(0x10, 0x80).poll_stat(0.1).nl()
