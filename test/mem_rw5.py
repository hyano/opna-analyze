import RsOPNA

def test_mem_read_repeat(start, stop, count, msg):
    rs.msg(msg)
    rs.out(0x10, 0x00).out(0x10, 0x80)
    rs.out(0x00, 0x30).out(0x01, 0x02)
    rs.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    rs.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    rs.nl()
    rs.mrd(count).nl()
    rs.out(0x00, 0x00).out(0x10, 0x80).nl()


rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
1. WRITE ADDRESS 0000-0000 (00-1F)
2. WRITE ADDRESS 0fff-1000 (40-7F)
3. WRITE ADDRESS 0fff-0xfff x 2 (80-9F/A0-BF)
    START ADDRESSに戻ることが確認できる
    STOP ADDRESSに到達したときにEOSビットが1になる
4. WRITE ADDRESS 1fff-1fff (C0-DF)

書き込み後のメモリの状態
    0000 00-1F
    0fff A0-BF
    1000 60-7F
    1fff C0-DF

5. READ ADDRESS 0fff-0xfff x 2
    データはA0-BF(EOS),BF,BF,A0-BF(EOS)
    ダミーリード(7F,7F,A0,A1)
    STOP ADDRESS後にダミーリードが挟まる(BF,BF)
    STOP ADDRESSに到達したときにEOSビットが1になる

5. READ ADDRESS 0fff-0xfff x 2 REPEAT
    REPEATビットが1の時の挙動を確認するテスト
    データはA0-BF(EOS),BF,A0-BF(EOS),BF
    ダミーリード(7F,7F,A0,A1)
    STOP ADDRESS後にダミーリードが「1バイトだけ」挟まる(BF)
    STOP ADDRESSに到達したときにEOSビットが1になる

全体
    REPEATビットが1の場合、繰返し時のダミーリードが1回になる

'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0000, 0x00, 32, "1. WRITE ADDRESS 0000-0000 (00-1F)")
rs.seq_mem_write(0x0fff, 0x1000, 0x40, 64, "2. WRITE ADDRESS 0fff-1000 (40-7F)")
rs.seq_mem_write(0x0fff, 0x0fff, 0x80, 64, "3. WRITE ADDRESS 0fff-0xfff x 2 (80-9F/A0-BF)")
rs.seq_mem_write(0x1fff, 0x1fff, 0xc0, 32, "4. WRITE ADDRESS 1fff-1fff (C0-DF)")

rs.reset()
rs.seq_mem_read(0x0fff, 0x0fff, 68, "5. READ ADDRESS 0fff-0xfff x 2")
rs.reset()
test_mem_read_repeat(0x0fff, 0x0fff, 68, "6. READ ADDRESS 0fff-0xfff x 2 REPEAT")
