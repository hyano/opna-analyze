import RsOPNA

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
READシーケンスを途中で止めた場合のダミーリードの確認

1. WRITE ADDRESS 0000-0001 (00-3F)
2. WRITE ADDRESS 0fff-0fff (A0-BF)

書き込み後のメモリの状態
    0000 00-1F
    0001 20-3F
    0fff A0-BF

3. READ ADDRESS 0000-0001 (34B)
    READシーケンスの途中で止める。
    データは00-1F(途中で中止)
    ダミーリード(BF, BF)

4. READ ADDRESS 0fff-0fff
    データはA0-BF(EOS)
    ダミーリード(20, 21)

全体
    READシーケンスを途中で止めた場合、次のダミーリードはバッファに読み込まれていたデータになる。
'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0001, 0x00, 64, "1. WRITE ADDRESS 0000-0001 (00-3F)")
rs.seq_mem_write(0x0fff, 0x0fff, 0xA0, 32, "2. WRITE ADDRESS 0fff-0fff (A0-BF)")

rs.seq_mem_read(0x0000, 0x0001, 32+2, "3. READ ADDRESS 0000-0001 (34B)")
rs.reset()
rs.seq_mem_read(0x0fff, 0x0fff, 32+2, "4. READ ADDRESS 0fff-0fff")
