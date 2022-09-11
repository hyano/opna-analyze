import RsOPNA

def test_seq_mem_write_without_record(self, start, stop, data, count, msg):
    control1 = 0x20 # REC=0
    self.msg(msg)
    self.out(0x10, 0x00).out(0x10, 0x80)
    self.out(0x00, control1).out(0x01, 0x02)
    self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    self.nl()
    self.mwr(data, count).nl()
    self.out(0x00, 0x00).out(0x10, 0x80).nl()
    return self


rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
REC=0でWRITEした時の挙動の確認

1. WRITE ADDRESS 0000-0001 (00-3F)

書き込み後のメモリの状態
    0000 00-1F
    0001 20-3F

2. READ ADDRESS 0000-0001 (32B)
    READシーケンスを途中で止めて、バッファの中身を20,21にする

3. WRITE ADDRESS 0000-0000 (40-5F) (REC=0)
    REC=1でWRITEする
    2バイト目以降、BRDY=0のまま変わらない
    EOSは1にならない
    MDEN信号は0のままで、メモリアクセスしていない

4. READ ADDRESS 0000-0001
    データとバッファの状態を確認する
    データは00-3F(EOS)
    ダミーリード(5F,21)

全体
    REC=0でWRITEしてもメモリの内容は変わらない
    2バイト書いた後にBRDYが0のままになる
    その後のREADではバッファの1バイト目が最後のWRITEデータ、2バイト目が元々バッファにあった2バイト目になる。
    BRDYはリセットで1になることを別の実験で確認した。

'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0001, 0x00, 64, "1. WRITE ADDRESS 0000-0001 (00-3F)")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 32+2, "2. READ ADDRESS 0000-0001 (32B)")
rs.reset()
test_seq_mem_write_without_record(rs, 0x0000, 0x0000, 0x40, 32, "3. WRITE ADDRESS 0000-0000 (40-5F) (REC=0)")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 64+2, "4. READ ADDRESS 0000-0001")
