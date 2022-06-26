import RsOPNA

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
ダミーリードのデータと演奏したデータの関係を調べるテスト

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

3. PLAY 0000

4. READ ADDRESS 0001-0002 (32Bx3 +2B)
    LIMIT ADDRESSにヒットしない、通常の読み出しの挙動の確認(LIMIT=ffff)
    ダミーリード(5F,5F)
    データは20-5F(EOS)
    STOP ADDRESSに到達したときにEOSビットが1になる
    STOP ADDRESS後にダミーリードが挟まる(5F,5F)
    データは20,...,3C,3D

5. PLAY 0001

6. READ ADDRESS 0001-0002 (32Bx3 +2B)
    LIMIT ADDRESSにヒットしない、通常の読み出しの挙動の確認(LIMIT=ffff)
    ダミーリード(5F,5F)
    データは20-5F(EOS)
    STOP ADDRESSに到達したときにEOSビットが1になる
    STOP ADDRESS後にダミーリードが挟まる(5F,5F)
    データは20,...,3C,3D

7. PLAY 0002

8. READ ADDRESS 0001-0002 (32Bx3 +2B)
    LIMIT ADDRESSにヒットしない、通常の読み出しの挙動の確認(LIMIT=ffff)
    ダミーリード(5F,5F)
    データは20-5F(EOS)
    STOP ADDRESSに到達したときにEOSビットが1になる
    STOP ADDRESS後にダミーリードが挟まる(5F,5F)
    データは20,...,3C,3D

全体
    STOP ADDRESSとLIMIT ADDRESSが同じ場合、先にSTOP ADDRESSがヒットする
    STOP ADDRESSにヒットした場合は、START ADDRESSに戻り、再度ダミーリードがかかる
    LIMIT ADDRESSがヒットした場合は、0番地に戻り、ダミーリードはかからない

'''

def play(adr, msg):
    rs.seq_play(adr, adr, int(512), 0xff, False, msg)
    rs.poll_stat(1.0)
    rs.seq_stop("STOP")


rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0002, 0x00, 32*3, "1. WRITE ADDRESS 0000-0002 (00-5F)")

rs.reset()
rs.seq_mem_read(0x0001, 0x0002, 32*3+2, "2. READ ADDRESS 0001-0002")

rs.reset()
play(0x0000, "3. PLAY ADDRESS 0000")
rs.reset()
rs.seq_mem_read(0x0001, 0x0002, 32*3+2, "4. READ ADDRESS 0001-0002")

rs.reset()
play(0x0001, "5. PLAY ADDRESS 0001")
rs.reset()
rs.seq_mem_read(0x0001, 0x0002, 32*3+2, "6. READ ADDRESS 0001-0002")

rs.reset()
play(0x0002, "7. PLAY ADDRESS 0002")
rs.reset()
rs.seq_mem_read(0x0001, 0x0002, 32*3+2, "8. READ ADDRESS 0001-0002")

