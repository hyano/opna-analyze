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
1. WRITE ADDRESS 0000-0001 (00-3F)
2. WRITE ADDRESS 0fff-1000 (40-7F)
3. WRITE ADDRESS 0fff-0xfff x 2 (80-9F/A0-BF)
    START ADDRESSに戻ることが確認できる
    STOP ADDRESSに到達したときにEOSビットが1になる
4. WRITE ADDRESS 1fff-1fff (C0-DF)

書き込み後のメモリの状態
    0000 00-1F
    0000 20-3F
    0fff A0-BF
    1000 60-7F
    1fff C0-DF

5. READ ADDRESS 0000-0000
    データは00-1F(EOS)
    ダミーリード(DF,DF,00,01)

6. READ ADDRESS 0fff-1000
    データはA0-BF,60-7F(EOS)
    ダミーリード(1F,1F,A0,A1)

7. READ ADDRESS 0fff-0xfff x 2
    データはA0-BF(EOS),BF,BF,A0-BF(EOS)
    ダミーリード(7F,7F,A0,A1)
    STOP ADDRESS後にダミーリードが挟まる(BF,BF)
    STOP ADDRESSに到達したときにEOSビットが1になる

8. READ ADDRESS 0fff- CHANGE START(1)
    読み出し後にSTART ADDRESSを0fffから1000に書き換えるテスト
    1バイト読んだ後で、STARTアドレスを1000に変更するが、変化はしない(ダミーリード中を狙う)
    データはA0-BF,60-7F(EOS),7F,7F,60-7F(EOS)
    STOP ADDRESSに到達したら、新しいSTART ADDRESS(1000)に戻ることを確認
    ダミーリード(7F,7F,A0,A1)
    STOP ADDRESS後にダミーリードが挟まる(7F,7F)
    STOP ADDRESSに到達したときにEOSビットが1になる

9. READ ADDRESS 0fff- CHANGE START(10)
    読み出し後にSTART ADDRESSを0fffから1000に書き換えるテスト
    10バイト読んだ後で、STARTアドレスを1000に変更するが、変化はしない(ダミーリード後を狙う)
    データはA0-BF,60-7F(EOS),7F,7F,60-7F(EOS)
    STOP ADDRESSに到達したら、新しいSTART ADDRESS(1000)に戻ることを確認
    ダミーリード(7F,7F,A0,A1)
    STOP ADDRESS後にダミーリードが挟まる(7F,7F)
    STOP ADDRESSに到達したときにEOSビットが1になる

10. READ ADDRESS 0fff- CHANGE START(10/RESET)
    読み出し後にSTART ADDRESSを0fffから0000に書き換えるテスト
    10バイト読んだ後で、STARTアドレスを0000に変更するが、変化はしない(ダミーリード後を狙う)
    データはA0-BF,60-7F(EOS),7F,7F,00-1F(no EOS)
    STOP ADDRESSに到達したら、新しいSTART ADDRESS(0000)に戻ることを確認
    ダミーリード(7F,7F,A0,A1)
    STOP ADDRESS後にダミーリードが挟まる(7F,7F)
    STOP ADDRESSに到達したときにEOSビットが1になる
    折り返した後、STOP ADDRESSに到達する前に読み出しを止めるので、その後リセットで復帰させる

11. READ ADDRESS 0fff- CHANGE STOP
    読み出し後にSTOP ADDRESSを0fffから1000に書き換えるテスト
    10バイト読んだ後で、STOPアドレスを1000に変更すると、0fff終端に達しても、止まらず進む
    データはA0-BF,60-7F(EOS),7F,7F,A0-BF,60-7F(EOS)
    ダミーリード(20,21,A0,A1)

12. READ ADDRESS 1fff-1fff
    データはC0-DF(EOS)
    ダミーリード(7F,7F,C0,C1)

13. READ ADDRESS 0000-0000 (10 WRITE)
    10バイト読み出し後、レジスタ08にダミーデータ(0xCC)を書き込み、その後読み出しを継続する
    データは00-07,(XX),09-1F(EOS),1F,1F,00-1F(EOS)
    ダミーデータの書き込みでアドレスが進んでいるが、書き込みは行われないことを2周目のREADで確認できる
    MDEN信号は動いているが読み出しになっているのではないかと推測する

'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0001, 0x00, 64, "1. WRITE ADDRESS 0000-0001 (00-3F)")
rs.seq_mem_write(0x0fff, 0x1000, 0x40, 64, "2. WRITE ADDRESS 0fff-1000 (40-7F)")
rs.seq_mem_write(0x0fff, 0x0fff, 0x80, 64, "3. WRITE ADDRESS 0fff-0xfff x 2 (80-9F/A0-BF)")
rs.seq_mem_write(0x1fff, 0x1fff, 0xc0, 32, "4. WRITE ADDRESS 1fff-1fff (C0-DF)")

rs.seq_mem_read(0x0000, 0x0000, 34, "5. READ ADDRESS 0000-0000")
rs.seq_mem_read(0x0fff, 0x1000, 66, "6. READ ADDRESS 0fff-1000")
rs.seq_mem_read(0x0fff, 0x0fff, 68, "7. READ ADDRESS 0fff-0xfff x 2")
#test_mem_read_repeat(0x0fff, 0x0fff, 68, "READ ADDRESS 0fff-0xfff x 2 REPEAT")
test_mem_read_start(0x0fff, 0x1000, 0x1000, 1, 66+34-1, "8. READ ADDRESS 0fff- CHANGE START(1)")
test_mem_read_start(0x0fff, 0x1000, 0x1000, 10, 66+34-10, "9. READ ADDRESS 0fff- CHANGE START(10)")
test_mem_read_start(0x0fff, 0x0000, 0x1000, 10, 66+34-10, "10. READ ADDRESS 0fff- CHANGE START(10/RESET)")
rs.reset()
test_mem_read_stop(0x0fff, 0x0fff, 0x1000, 10, 66+66-10, "11. READ ADDRESS 0fff- CHANGE STOP")
rs.seq_mem_read(0x1fff, 0x1fff, 34, "12. READ ADDRESS 1fff-1fff")


rs.msg("READ / WRITE MIX")
rs.reset()
test_mem_read_write(0x0000, 0x0000, 10, 68-10-1, "13. READ ADDRESS 0000-0000 (10 WRITE)")


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
