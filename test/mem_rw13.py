import RsOPNA

def test_seq_mem_read(self, start, stop, count, msg):
    control1 = 0x20
    self.msg(msg)
    self.out(0x10, 0x00).out(0x10, 0x80)
    self.out(0x00, control1).out(0x01, 0x02)
    self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    self.nl()
    self.mrd(count).nl()
    self.out(0x00, 0x00).out(0x10, 0x80).nl()


rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
READシーケンスを途中で止めた場合のダミーリードの確認

1. WRITE ADDRESS 0000-0001 (00-3F)
2. WRITE ADDRESS 0fff-0fff (A0-BF)

書き込み後のメモリの状態
    0000 00-1F
    0001 20-3F
    0fff A0-BF

    last READ-> DUMMY READ
1   BF          BF 00
2   BF BF       00 01
3   BF 00       01 02
4   00 01       02 03

31  1B 1C       1D 1E
32  1C 1D       1E 1F
33  1D 1E       1F 1F
34  1E 1F*      1F 1F   *: EOS
35  1F*1F       1F 00   *: EOS
36  1F 1F       00 01
37  1F 00       01 02

全体
    直前のREADでバッファに読み込まれたデータがダミーリードで読み出される
'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0001, 0x00, 64, "1. WRITE ADDRESS 0000-0001 (00-3F)")
rs.seq_mem_write(0x0fff, 0x0fff, 0xA0, 32, "2. WRITE ADDRESS 0fff-0fff (A0-BF)")

testno =  3
for i in [1, 2, 3, 4, 31, 32, 33, 34, 35, 36, 37]:
    rs.reset()
    test_seq_mem_read(rs, 0x0000, 0x0000, i, "{0}. READ ADDRESS 0000-0000 ({1}B)".format(testno, i))
    testno += 1
    rs.reset()
    rs.seq_mem_read(0x0fff, 0x0fff, 32+2, "{0}. READ ADDRESS 0fff-0fff (DUMMY READ TEST)".format(testno))
    testno += 1

