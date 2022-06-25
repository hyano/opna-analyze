import RsOPNA

def test_mem_read_stop(start, stop, limit, count1, count2, msg):
    rs.msg(msg)
    rs.out(0x10, 0x00).out(0x10, 0x80)
    rs.out(0x00, 0x20).out(0x01, 0x02)
    rs.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    rs.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    rs.nl()
    rs.mrd(count1).nl()
    rs.seq_mem_limit(limit)
    rs.mrd(count2).nl()
    rs.out(0x00, 0x00).out(0x10, 0x80).nl()


rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
読み出し中のLIMIT ADDRESSの変更と反映のテスト

1. WRITE ADDRESS 0000-0002 (00-5F)

書き込み後のメモリの状態
    0000 00-1F
    0001 20-3F
    0002 40-5F

2. READ ADDRESS 0001-0002 CHANGE LIMIT (31)
    読み出し開始後にLIMIT ADDRESSをffffから0001に書き換えるテスト
    31バイト読んだ後で、LIMITアドレスを0001に変更すると、33バイト目は0番地に戻る(LIMIT ADDRESS書き換えが有効)
    ダミーリード(5F,5F)
    データは20-3C
    LIMITアドレス書き換え
    データは3D,3E,3F,00,01,...,3E,3F

3. READ ADDRESS 0001-0002 CHANGE LIMIT (32)
    読み出し開始後にLIMIT ADDRESSをffffから0001に書き換えるテスト
    32バイト読んだ後で、LIMITアドレスを0001に変更しても、33バイト目は0番地に戻らない(LIMIT ADDRESS書き換えが無効)
    ダミーリード(00,01)
    データは20-3D
    LIMITアドレス書き換え
    データは3E,3F,40,41,...,5F(EOS),5F,5F,20,21,...,3C,3D

4. READ ADDRESS 0001-0002 CHANGE LIMIT (33)
    3と同様。
    ダミーリード(3E,3F)
    データは20-3E
    LIMITアドレス書き換え
    データは3F,40,41,...,5F(EOS),5F,5F,20,21,...,3D,3E

5. READ ADDRESS 0001-0002 CHANGE LIMIT (34)
    3と同様。
    ダミーリード(3F,00)
    データは20-3F
    LIMITアドレス書き換え
    データは40,41,...,5F(EOS),5F,5F,20,21,...,3E,3F

全体
    ダミーリード込みで32バイト目の読み出し時、
    つまり、メモリからの読み出しのタイミングで、LIMIT ADDRESSのチェックをしている。

'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0002, 0x00, 32*3, "1. WRITE ADDRESS 0000-0002 (00-5F)")

rs.seq_mem_limit(0xffff)
rs.reset()
test_mem_read_stop(0x0001, 0x0002, 0x0001, 31, 32*3+2-31, "2. READ ADDRESS 0001-0002 CHANGE LIMIT (31)")

rs.seq_mem_limit(0xffff)
rs.reset()
test_mem_read_stop(0x0001, 0x0002, 0x0001, 32, 32*3+2-32, "3. READ ADDRESS 0001-0002 CHANGE LIMIT (32)")

rs.seq_mem_limit(0xffff)
rs.reset()
test_mem_read_stop(0x0001, 0x0002, 0x0001, 33, 32*3+2-32, "4. READ ADDRESS 0001-0002 CHANGE LIMIT (33)")

rs.seq_mem_limit(0xffff)
rs.reset()
test_mem_read_stop(0x0001, 0x0002, 0x0001, 34, 32*3+2-32, "5. READ ADDRESS 0001-0002 CHANGE LIMIT (34)")

