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

def test_mem_read_start(start1, start2, stop, count1, count2, msg):
    rs.msg(msg)
    rs.out(0x10, 0x00).out(0x10, 0x80)
    rs.out(0x00, 0x20).out(0x01, 0x02)
    rs.out(0x02, start1 & 0xff).out(0x03, (start1 >> 8) & 0xff)
    rs.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    rs.nl()
    rs.mrd(count1).nl()
    rs.out(0x02, start2 & 0xff).out(0x03, (start2 >> 8) & 0xff)
    rs.mrd(count2).nl()
    rs.out(0x00, 0x00).out(0x10, 0x80).nl()

def test_mem_read_stop(start, stop1, stop2, count1, count2, msg):
    rs.msg(msg)
    rs.out(0x10, 0x00).out(0x10, 0x80)
    rs.out(0x00, 0x20).out(0x01, 0x02)
    rs.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    rs.out(0x04, stop1 & 0xff).out(0x05, (stop1 >> 8) & 0xff)
    rs.nl()
    rs.mrd(count1).nl()
    rs.out(0x04, stop2 & 0xff).out(0x05, (stop2 >> 8) & 0xff)
    rs.mrd(count2).nl()
    rs.out(0x00, 0x00).out(0x10, 0x80).nl()

def test_mem_read_write(start, stop, count1, count2, msg):
    rs.msg(msg)
    rs.out(0x10, 0x00).out(0x10, 0x80)
    rs.out(0x00, 0x20).out(0x01, 0x02)
    rs.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    rs.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    rs.nl()
    rs.mrd(count1).nl()
    rs.out(0x08, 0xcc).stat()
    rs.mrd(count2).nl()
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

5. READ ADDRESS 0fff- CHANGE STOP (31)
    読み出し後にSTOP ADDRESSを0fffから1000に書き換えるテスト
    31バイト読んだ後で、STOPアドレスを1000に変更すると、0fff終端に達しても、止まらず進む
    データはA0-BF,60-7F(EOS),7F,7F,A0-BF,60-7F(EOS)
    ダミーリード(DF,DF,A0,A1)

6. READ ADDRESS 0fff- CHANGE STOP (32)
    読み出し後にSTOP ADDRESSを0fffから1000に書き換えるテスト
    32バイト読んだ後で、STOPアドレスを1000に変更しても0fff終端に達しても、止まらず進む
    データはA0-BF(EOS),BF,BF,A0-BF,60-7F(EOS),7F,7F,A0-BF,60-7F(EOS)
    ダミーリード(7F,7F,A0,A1)

7. READ ADDRESS 0fff- CHANGE STOP (33)
    6と同様の結果

8. READ ADDRESS 0fff- CHANGE STOP (34)
    6と同様の結果

'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0000, 0x00, 32, "1. WRITE ADDRESS 0000-0000 (00-1F)")
rs.seq_mem_write(0x0fff, 0x1000, 0x40, 64, "2. WRITE ADDRESS 0fff-1000 (40-7F)")
rs.seq_mem_write(0x0fff, 0x0fff, 0x80, 64, "3. WRITE ADDRESS 0fff-0xfff x 2 (80-9F/A0-BF)")
rs.seq_mem_write(0x1fff, 0x1fff, 0xc0, 32, "4. WRITE ADDRESS 1fff-1fff (C0-DF)")

test_mem_read_stop(0x0fff, 0x0fff, 0x1000, 31, 66+66-31, "5. READ ADDRESS 0fff- CHANGE STOP (31)")
rs.reset()
test_mem_read_stop(0x0fff, 0x0fff, 0x1000, 32, 34+66+66-32, "6. READ ADDRESS 0fff- CHANGE STOP (32)")
rs.reset()
test_mem_read_stop(0x0fff, 0x0fff, 0x1000, 33, 34+66+66-33, "7. READ ADDRESS 0fff- CHANGE STOP (33)")
rs.reset()
test_mem_read_stop(0x0fff, 0x0fff, 0x1000, 34, 34+66+66-34, "8. READ ADDRESS 0fff- CHANGE STOP (34)")
rs.reset()


'''
rs.msg("LIMIT (0x0fff)")
rs.seq_mem_limit(0x0fff)
rs.seq_mem_read(0x0fff, 0x0fff, 68, "READ ADDRESS 0fff-0xfff x 2 (w/LIMIT)")
rs.seq_mem_read(0x0fff, 0x0000, 66, "READ ADDRESS 0fff-0000 (w/LIMIT)")

rs.msg("LIMIT (0x00ff)")
rs.seq_mem_limit(0x00ff)
rs.seq_mem_read(0x0fff, 0x0fff, 68, "READ ADDRESS 0fff-0xfff x 2 (w/LIMIT)")
rs.seq_mem_read(0x0fff, 0x1000, 66, "READ ADDRESS 0fff-1000 (w/LIMIT)")
'''
