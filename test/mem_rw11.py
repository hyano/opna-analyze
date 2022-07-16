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

1. WRITE ADDRESS 0000-0000 (00-1F) after RESET
    32バイト目は、MDENが2回アサートされている
2. WRITE ADDRESS 0fff-0fff (40-5F) after RESET
    32バイト目は、MDENが2回アサートされている


3. READ ADDRESS 0000-0000
    ダミーリード(5F,40) (40は0fffの先頭)
    データは00-1F(EOS)


メモリの状態
    0000 00-1F
    0fff 40-5F

全体
    REPEATで先頭に戻る時、メモリの読み出しも発生している?

'''

rs.seq_mem_limit(0xffff)
rs.reset()
test_mem_write(rs, 0x0000, 0x0000, 0x00, 32, "1. WRITE ADDRESS 0000-0000 (00-1F) after RESET")
rs.reset()
test_mem_write(rs, 0x0fff, 0x0fff, 0x40, 32, "2. WRITE ADDRESS 0fff-0fff (40-5F) after RESET")

rs.reset()
rs.seq_mem_read(0x0000, 0x0000, 34, "3. READ ADDRESS 0000-0000")
