import RsOPNA
import time

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
LIMIT ADDRESS到達時の挙動の確認

書き込み後のメモリの状態
    0000-0001 無音データ(先頭にマーク(7f 7f))
    0002-0003 テスト波形(先頭)


以下の関係で再生し、0番地に戻る際の挙動を確認する。
TEST 0
    START = 0000
    LIMIT = 0000
    STOP  = 0001

TEST 1
    START = 0002
    LIMIT = 0002
    STOP  = 0003
'''

rs.seq_mem_limit(0xffff)

def mem_set(pat, adr, msg):
    rs.seq_mem_fill_pat(adr*2, adr*2+1, pat, 32 * 0x02, msg)


def test(adr, rep, msg):
    rs.seq_mem_limit(adr*2)
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
silence[0] = 0x7f
silence[1] = 0x7f
pat = silence
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
pat = pat_orig
mem_set(pat, t, "PAT {:d}".format(t))
t+=1
'''
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
'''

for i in range(0, t):
    test(i, False, "TEST {:d}".format(i))

for i in range(0, t):
    test(i, True, "TEST REPEAT {:d}".format(i))

