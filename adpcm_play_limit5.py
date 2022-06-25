import RsOPNA
import time

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
LIMIT ADDRESS到達時の挙動の確認
STOP ADDRESSと同じにして、どちらが先に判定されるかを確認する
データサイズを32Bに縮小

書き込み後のメモリの状態
    0000-0000 無音データ(先頭にマーク(7f 7f))
    0001-0001 テスト波形(先頭)


以下の関係で再生し、0番地に戻る際の挙動を確認する。
TEST=1
    START = 0000
    LIMIT = 0000
    STOP  = 0000

TEST=2
    START = 0001
    LIMIT = 0001
    STOP  = 0001
'''

rs.seq_mem_limit(0xffff)

def mem_set(pat, adr, msg):
    rs.seq_mem_fill_pat(adr, adr, pat, 32, msg)


def test(adr, rep, msg):
    rs.seq_mem_limit(adr)
    rs.seq_play(adr, adr, int(512), 0xff, rep, "PLAY " + msg)
    #time.sleep(1.0)
    rs.poll_stat(1.0)
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

