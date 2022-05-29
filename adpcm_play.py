import RsOPNA
import time

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

rs.seq_mem_limit(0xffff)

def mem_set(pat, adr, msg):
    rs.seq_mem_fill_pat(adr, adr, pat, 32 * 0x01, msg)


def test(adr, rep, msg):
    rs.seq_play(adr, adr, int(512), 0xc0, rep, "PLAY " + msg)
    time.sleep(0.5)
    rs.seq_stop("STOP")
    #time.sleep(0.2)

silence = []
for i in range(32):
    silence.append(0x80)

pat_orig = [
    0x77, 0x77,
    0x77, 0xcb,
    0x43, 0xcb,
    0x43, 0xcb,

    0x43, 0xcb,
    0x43, 0xcb,
    0x43, 0xcb,
    0x43, 0xcb,

    0x43, 0xcb,
    0x43, 0xcb,
    0x43, 0xcb,
    0x43, 0xcb,

    0x43, 0xcb,
    0x43, 0xcb,
    0x43, 0xcb,
    0x43, 0xcb,
]

t=0
pat = silence
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
pat = pat_orig
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
pat[31] = 0x77
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
pat[31] = 0xff
mem_set(pat, t, "PAT {:d}".format(t))
t+=1

pat[30] = 0x4f
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
pat[30] = 0xf3
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
pat[30] = 0xff
mem_set(pat, t, "PAT {:d}".format(t))
t+=1

pat[29] = 0x77
mem_set(pat, t, "PAT {:d}".format(t))
t+=1


for i in range(0, t):
    test(i, False, "TEST {:d}".format(i))

for i in range(0, t):
    test(i, True, "TEST REPEAT {:d}".format(i))

