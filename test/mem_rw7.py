import RsOPNA
import time

def test_mem_write(self, start, stop, data, count, msg):
    control1 = 0x60 # REPEAT(bit.4 = 0)
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
REPEATビットを"0"にした状態でメモリを書き込むテスト

0. CLEAR MEMORY

1. WRITE ADDRESS 0000-0000 (00-1F) after RESET
2. WRITE ADDRESS 0fff-1000 (40-7F) after RESET
3. WRITE ADDRESS 0fff-0fff x 2 (80-9F/A0-BF) after RESET
4. WRITE ADDRESS 1fff-1fff (C0-DF)


5. READ ADDRESS 0000-0000
    ダミーリード(DF,61)
    データは00-1F(EOS)

6. READ ADDRESS 0fff-1000
    ダミーリード(1F,1F)
    データは80-9F,60-7F(EOS)

7. READ ADDRESS 1fff-1fff
    ダミーリード(7F,7F)
    データは00-00(EOS)

メモリの状態
    0000 00-1F
    0fff A0-BF
    1000 60-7F
    1fff C0-DF

全体
    異常動作がないことの確認なので特に新しいことなし。
    考察は、mem_rw8のコメント。



'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_fill(0x0000, 0x0000, 0x00, 32, "CLEAR ADDRESS 0000-0000")
rs.seq_mem_fill(0x0fff, 0x1000, 0x00, 64, "CLEAR ADDRESS 0fff-1000")
rs.seq_mem_fill(0x1fff, 0x1fff, 0x00, 32, "CLEAR ADDRESS 1fff-1fff")
rs.seq_mem_read(0x0000, 0x0000, 34, "READ ADDRESS 0000-0000")
rs.seq_mem_read(0x0fff, 0x1000, 66, "READ ADDRESS 0fff-1000")
rs.seq_mem_read(0x1fff, 0x1fff, 34, "READ ADDRESS 1fff-1fff")

time.sleep(0.5)

rs.reset()
test_mem_write(rs, 0x0000, 0x0000, 0x00, 32, "1. WRITE ADDRESS 0000-0000 (00-1F) after RESET")
rs.reset()
test_mem_write(rs, 0x0fff, 0x1000, 0x40, 64, "2. WRITE ADDRESS 0fff-1000 (40-7F) after RESET")
rs.reset()
test_mem_write(rs, 0x0fff, 0x0fff, 0x80, 64, "3. WRITE ADDRESS 0fff-0fff x 2 (80-9F/A0-BF) after RESET")
test_mem_write(rs, 0x1fff, 0x1fff, 0xc0, 32, "4. WRITE ADDRESS 1fff-1fff (C0-DF)")

rs.reset()
rs.seq_mem_read(0x0000, 0x0000, 34, "5. READ ADDRESS 0000-0000")
rs.seq_mem_read(0x0fff, 0x1000, 66, "6. READ ADDRESS 0fff-1000")
rs.seq_mem_read(0x1fff, 0x1fff, 34, "7. READ ADDRESS 1fff-1fff")
