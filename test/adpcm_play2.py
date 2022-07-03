import RsOPNA
import time

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

rs.seq_mem_limit(0xffff)

def mem_set(pat, adr, msg):
    rs.seq_mem_fill_pat(adr*2, adr*2+1, pat, 32 * 0x02, msg)


def test(adr, rep, msg):
    rs.seq_play(adr*2, adr*2+1, int(512), 0xff, rep, "PLAY " + msg)
    #time.sleep(1.0)
    rs.poll_stat(1.0)
    rs.seq_stop("STOP")
    #time.sleep(0.2)

silence = []
for i in range(64):
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
pat[63] = 0x77
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
pat[63] = 0xff
mem_set(pat, t, "PAT {:d}".format(t))
t+=1

pat[62] = 0x4f
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
pat[62] = 0xf3
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
pat[62] = 0xff
mem_set(pat, t, "PAT {:d}".format(t))
t+=1

pat[61] = 0x77
mem_set(pat, t, "PAT {:d}".format(t))
t+=1


for i in range(0, t):
    test(i, False, "TEST {:d}".format(i))

for i in range(0, t):
    test(i, True, "TEST REPEAT {:d}".format(i))

