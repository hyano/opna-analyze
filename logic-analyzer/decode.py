import sys

prev = 0
clk = 0
sd = 0
smp1 = 0
smp2 = 0

sample = 0
sample_1 = 0
sample_2 = 0

def da(data):
    if data & 0x8000 != 0:
        data = -(0x10000 - data)
    return data


while True:
    b = sys.stdin.buffer.read(1)
    if b == b'':
        break
    data = int.from_bytes(b, 'little')
    diff = prev ^ data
    if diff == 0:
        continue
    prev = data

    clk = data & 1
    sd = (data >> 1) & 1
    smp1 = (data >> 2) & 1
    smp2 = (data >> 3) & 1

    if ((diff & 1) != 0) and (clk == 0):
        sample = (sample >> 1) | (sd << 15)

    if (diff & 8 != 0) and (smp2 == 0):
        sample_1 = sample ^ 0x8000
    if (diff & 4 != 0) and (smp1 == 0):
        sample_2 = sample ^ 0x8000
        print("{:016b},{:016b}".format(sample_1, sample_2))
