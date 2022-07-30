import RsOPNA

def test_seq_mem_read_switch_record(self, start, stop, count1, count2, repeat, msg):
    if repeat:
        control1 = 0x70
    else:
        control1 = 0x60
    self.msg(msg)
    self.out(0x10, 0x00).out(0x10, 0x80)
    self.out(0x00, control1).out(0x01, 0x02)
    self.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    self.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    self.nl()
    if (count1 > 0):
        self.mrd(count1).nl()

    if repeat:
        control1 = 0x30
    else:
        control1 = 0x20
    self.out(0x00, control1) # REC=0

    if (count2 > 0):
        self.mrd(count2).nl()
    self.out(0x00, 0x00).out(0x10, 0x80).nl()


rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

'''
REC=1でREADした時の挙動の確認 (途中でREC=0に変更する)

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

5-. READ ADDRESS 0000-0000 (REC=1(xxB)/REPEAT=0) (xx=1,2,3,8)
    REC=1/REPEAT=0でREADする
    2バイト目からBRDY=0になる
    この区間ではMDEN信号は0のままで、メモリアクセスしていない
    xxB読んだところでREC=0/REPEAT=0に変更する
    この後のREADで、MDENが2連続で1になる
    xx=1B
        REC=0: 20
        REC=1: 20,00,01...1E,1F(EOS),1F,1F,00,01,02,03,04,05
    xx=2B
        REC=0: 20,20
        REC=1: 20,00,01...1E,1F(EOS),1F,1F,00,01,02,03,04
    xx=3B
        REC=0: 20,20,20
        REC=1: 20,00,01...1E,1F(EOS),1F,1F,00,01,02,03
    xx=8B
        REC=0: 20,20,20,20,20,20,20,20
        REC=1: 20,00,01...1E,1F(EOS),1F

13-. READ ADDRESS 0000-0000 (REC=1(xxB)/REPEAT=1) (xx=1,2,3,8)
    REC=1/REPEAT=1でREADする
    2バイト目からBRDY=0になる
    この区間ではMDEN信号は0のままで、メモリアクセスしていない
    xxB読んだところでREC=0/REPEAT=1に変更する
    この後のREADで、MDENが2連続で1になる
    xx=1B
        REC=0: 20
        REC=1: 20,00,01...1E,1F(EOS),1F,00,01,02,03,04,05,06
    xx=2B
        REC=0: 20,20
        REC=1: 20,00,01...1E,1F(EOS),1F,00,01,02,03,04,05
    xx=3B
        REC=0: 20,20,20
        REC=1: 20,00,01...1E,1F(EOS),1F,00,01,02,03,04
    xx=8B
        REC=0: 20,20,20,20,20,20,20,20
        REC=1: 20,00,01...1E,1F(EOS),1F


全体
    REC=1でREADシーケンスを開始し、途中でREC=0に変更すると、メモリREADが開始される
    切り替え後の最初のREADで、メモリリードが2回発行される(MDEN信号で確認)
    切り替えが1バイト目の後であれば、通常のREADシーケンスと同じバイト数になる

'''

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0001, 0x00, 64, "1. WRITE ADDRESS 0000-0001 (00-3F)")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 32+2, "2. READ ADDRESS 0000-0001 (32B)")
rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 64+2, "3. READ ADDRESS 0000-0000")

testno = 4
for i in [1, 2, 3, 8]:
    rs.reset()
    rs.seq_mem_read(0x0000, 0x0001, 32+2, "{0}. READ ADDRESS 0000-0001 (32B)".format(testno))
    testno += 1
    rs.reset()
    test_seq_mem_read_switch_record(rs, 0x0000, 0x0000, i, 32+2+8 - i, False, "{0}. READ ADDRESS 0000-0000 (REC=1({1}B)->0/REPEAT=0)".format(testno, i))
    testno += 1

for i in [1, 2, 3, 8]:
    rs.reset()
    rs.seq_mem_read(0x0000, 0x0001, 32+2, "{0}. READ ADDRESS 0000-0001 (32B)".format(testno))
    testno += 1
    rs.reset()
    test_seq_mem_read_switch_record(rs, 0x0000, 0x0000, i, 32+2+8 - i, True, "{0}. READ ADDRESS 0000-0000 (REC=1({1}B)->0/REPEAT=1)".format(testno, i))
    testno += 1

rs.reset()
rs.seq_mem_read(0x0000, 0x0001, 64+2, "{0}. READ ADDRESS 0000-0001".format(testno))
