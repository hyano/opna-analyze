import RsOPNA
import time

def test_mem_write(self, start, stop, data, count, msg):
    control1 = 0x70 # REPEAT(bit.4 = 1)
    self.msg(msg)
    self.out(0x10, 0x00).out(0x10, 0x80)
    self.out(0x00, control1).out(0x01, 0x02)
    self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    self.nl()
    self.mwr(data, count).nl()
    self.out(0x00, 0x00).out(0x10, 0x80).nl()


rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
REPEATビットを"1"にした状態でメモリを書き込むテスト
その後のダミーリードの確認

0. CLEAR MEMORY

1. WRITE ADDRESS 0000-0000 (00-1F)
    32バイト目は、MDENが2回アサートされている

X. WRITE ADDRESS 0fff-0fff (40-5F)
    32バイト目は、MDENが2回アサートされている

メモリの状態
    0000 00-1F
    0fff 40-5F

    last WRITE->DUMMY READ
32  5E 5F*      5F 40
33  5F*60       60 41
34  60 61       61 42
35  61 62       62 43

メモリの状態
    0000 00-1F
    0fff 40-5F

全体
    REPEATで先頭で戻った後は、メモリの書き換えはされておらず、読み出しに切り替わっている?

'''

rs.seq_mem_limit(0xffff)
rs.reset()
test_mem_write(rs, 0x0000, 0x0000, 0x00, 32, "1. WRITE ADDRESS 0000-0000 (00-1F)")

testno = 2
for i in [0, 1, 2, 3]:
    rs.reset()
    test_mem_write(rs, 0x0fff, 0x0fff, 0x40, 32 + i, "{0}. WRITE ADDRESS 0fff-0fff (40-5F...) ({1}B)".format(testno, 32 + i))
    testno += 1
    rs.reset()
    rs.seq_mem_read(0x0000, 0x0000, 34, "{0}. READ ADDRESS 0000-0000".format(testno))
    testno += 1

rs.reset()
rs.seq_mem_read(0x0fff, 0x0fff, 34, "{0}. READ ADDRESS 0fff-0fff".format(testno))
