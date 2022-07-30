import RsOPNA

def test_seq_mem_read_with_record(self, start, stop, count, msg):
    self.msg(msg)
    self.out(0x10, 0x00).out(0x10, 0x80)
    self.out(0x00, 0x60).out(0x01, 0x02)
    self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    self.nl()
    if (count > 0):
        self.mrd(count).nl()
    self.out(0x00, 0x00).out(0x10, 0x80).nl()


rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
REC=1でREADした時の挙動の確認 (バッファが空の状態から)

1. WRITE ADDRESS 0000-0001 (00-3F)

書き込み後のメモリの状態
    0000 00-1F
    0001 20-3F

2. READ ADDRESS 0000-0001 (32B)
    READシーケンスを途中で止めて、バッファの中身を20,21にする

3. READ ADDRESS 0000-0000
    バッファの中身が20,21になることを確認する
    データは00-3F(EOS)
    ダミーリード(20,21)

4. READ ADDRESS 0000-0001 (32B)
    READシーケンスを途中で止めて、バッファの中身を20,21にする

5. READ ADDRESS 0000-0000 (REC=1)
    REC=1でREADする
    2バイト目以降、BRDY=0のまま変わらない
    EOSは1にならない
    MDEN信号は0のままで、メモリアクセスしていない
    データは20-20
    ダミーリード(20,20)

6. READ ADDRESS 0000-0000 (REC=1)
    REC=1でREADする
    2バイト目以降、BRDY=0のまま変わらない
    EOSは1にならない
    MDEN信号は0のままで、メモリアクセスしていない
    データは20-20
    ダミーリード(20,20)

7. READ ADDRESS 0000-0001
    データとバッファの状態を確認する
    データは00-3F(EOS)
    ダミーリード(20,20)

全体
    バッファが空の状態からREC=1でREADすると、バッファにデータが入った状態から始まる
    2バイト読んだところでBRDYは0になり、バッファが空になる

'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0001, 0x00, 64, "1. WRITE ADDRESS 0000-0001 (00-3F)")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 32+2, "2. READ ADDRESS 0000-0001 (32B)")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 64+2, "3. READ ADDRESS 0000-0000")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 32+2, "4. READ ADDRESS 0000-0001 (32B)")
rs.reset()
test_seq_mem_read_with_record(rs, 0x0000, 0x0000, 32+2, "5. READ ADDRESS 0000-0000 (REC=1)")
rs.reset()
test_seq_mem_read_with_record(rs, 0x0000, 0x0000, 32+2, "6. READ ADDRESS 0000-0000 (REC=1)")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 64+2, "7. READ ADDRESS 0000-0001")
