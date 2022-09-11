import RsOPNA

def test_seq_mem_write_without_record(self, start, stop, data, count, msg):
    control1 = 0x60 # REC=1
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
REC=1でWRITEした時の挙動の確認 (REC=0との比較用)

1. WRITE ADDRESS 0000-0001 (00-3F)

書き込み後のメモリの状態
    0000 00-1F
    0001 20-3F

2. READ ADDRESS 0000-0001 (32B)
    READシーケンスを途中で止めて、バッファの中身を20,21にする

3. WRITE ADDRESS 0000-0000 (40-5F) (REC=1)
    REC=1でWRITEする
    通常のWRITEと同じ挙動で、最後はEOS=1になる

4. READ ADDRESS 0000-0001
    データとバッファの状態を確認する
    データは40-5F(EOS)
    ダミーリード(5F,5F)

全体
    mem_rw20との比較用。REC=1でメモリの内容が書き変わることを確認できる。
    ダミーリードでは、最後に書き込んだデータが2バイト出てくる。

'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0001, 0x00, 64, "1. WRITE ADDRESS 0000-0001 (00-3F)")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 32+2, "2. READ ADDRESS 0000-0001 (32B)")
rs.reset()
test_seq_mem_write_without_record(rs, 0x0000, 0x0000, 0x40, 32, "3. WRITE ADDRESS 0000-0000 (40-5F) (REC=1)")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 64+2, "4. READ ADDRESS 0000-0001")
