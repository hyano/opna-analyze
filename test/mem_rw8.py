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

0. CLEAR MEMORY

1. WRITE ADDRESS 0000-0000 (00-1F) after RESET
    32バイト目は、MDENが2回アサートされている
2. WRITE ADDRESS 0fff-1000 (40-7F) after RESET
    64バイト目は、MDENが2回アサートされている
3. WRITE ADDRESS 0fff-0fff x 2 (80-9F/A0-BF) after RESET
    32バイト目(1回目にSTOP ADDRESSに到達他時)EOSビットが1になる
    32バイト目は、MDENが2回アサートされている
    その後はメモリに書き込みできていない様子
    メモリに書けていない時もMDENはアサートされている
    63バイト目で、EOSビットが1になる
    63バイト目は、MDENが2回アサートされている
    64バイト目は、MDENが1回アサートされている

4. WRITE ADDRESS 1fff-1fff (C0-DF)
    リセットがないとメモリに書き込みできていない様子
    メモリに書けていない時もMDENはアサートされている
    32バイト全て、MDENが1回アサートされている
    32バイト目(STOP ADDRESSに到達他時)にもEOSビットは1にならない


5. READ ADDRESS 0000-0000
    ダミーリード(DF,61) (61がどこから来ているか不明)
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
    1fff 00-00

全体
    REPEATビットが1でメモリ書き込みをSTOP ADDRESSまで行うと、状態が不安定になり、その後書き込みが行われない。
    MDENはアサートされており、何が起きているかは詳細調査必要か(/WEを見た方が良い)。
    書き込みできていない場合もそのデータがダミーリードでは値は観測されるのでOPNAには残っている(REPEAT=0の時と同じ)。
    RESET(コントロールレジスタ1($00)のbit.0を1)で回復する。

メモリの状態(REPEATビットでの違い)
    TEST    mem_rw7 mem_rw8
    REPEAT  0       1
    0000    00-1F   00-1F
    0fff    A0-BF   80-9F   REPEAT=1では、2周目が転送できていない
    1000    60-7F   60-7F
    1fff    C0-DF   00-00   REPEAT=1では転送できていない

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
