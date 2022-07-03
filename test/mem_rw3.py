import RsOPNA

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
STOP ADDRESSとLIMIT ADDRESSのどちらが先にチェックされるかのテスト

1. WRITE ADDRESS 0000-0002 (00-5F)

書き込み後のメモリの状態
    0000 00-1F
    0001 20-3F
    0002 40-5F

2. READ ADDRESS 0001-0002 (32Bx3 +2B)
    LIMIT ADDRESSにヒットしない、通常の読み出しの挙動の確認(LIMIT=ffff)
    ダミーリード(5F,5F)
    データは20-5F(EOS)
    STOP ADDRESSに到達したときにEOSビットが1になる
    STOP ADDRESS後にダミーリードが挟まる(5F,5F)
    データは20,...,3C,3D

3. READ ADDRESS 0001-0002 (LIMIT=0001) (32Bx3 +2B)
    LIMIT ADDRESSにヒットする場合の読み出しの挙動の確認(LIMIT=0001)
    ダミーリード(3E,3F)
    データは20-3F
    LIMIT ADDRESSにヒットして0000番地に戻る
    データは00-3F

4. READ ADDRESS 0001-0001 (LIMIT=0001) (32Bx3 +2B)
    LIMIT ADDRESSをSTOP ADDRESSが同じ場合のの読み出しの挙動の確認(LIMIT=0001)
    ダミーリード(00,01)
    データは20-3F(EOS)
    先にSTOP ADDRESSにヒットし、LIMIT ADDRESSにヒットしない
    ダミーリード(3F,3F)
    データは20-3F(EOS)
    先にSTOP ADDRESSにヒットし、LIMIT ADDRESSにヒットしない
    ダミーリード(3F,3F)
    データは20-3B

全体
    STOP ADDRESSとLIMIT ADDRESSが同じ場合、先にSTOP ADDRESSがヒットする
    STOP ADDRESSにヒットした場合は、START ADDRESSに戻り、再度ダミーリードがかかる
    LIMIT ADDRESSがヒットした場合は、0番地に戻り、ダミーリードはかからない

'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0002, 0x00, 32*3, "1. WRITE ADDRESS 0000-0002 (00-5F)")

rs.reset()
rs.seq_mem_read(0x0001, 0x0002, 32*3+2, "2. READ ADDRESS 0001-0002")

rs.reset()
rs.seq_mem_limit(0x0001)
rs.seq_mem_read(0x0001, 0x0002, 32*3+2, "3. READ ADDRESS 0001-0002 (LIMIT=0001)")

rs.reset()
rs.seq_mem_limit(0x0001)
rs.seq_mem_read(0x0001, 0x0001, 32*3+2, "4. READ ADDRESS 0001-0001 (LIMIT=0001)")

