import RsOPNA
import time

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

def test(adr, msg):
    rs.msg(msg)
    rs.out0(0x10, 0x00 | (1 << i))
    time.sleep(1.0)
    rs.out0(0x10, 0x80 | (1 << i)).nl()
    time.sleep(0.5)
    rs.out0(0x10, 0x00 | (1 << i))
    rs.out0(0x10, 0x80 | (1 << i)).nl()
    time.sleep(0.5)

rs.out0(0x11, 0x3f)
for i in range(0, 6):
    rs.out0(0x18 + i, 0xc0 | 0x1f)

for i in range(0, 6):
    test(i, "TEST {:d}".format(i))
