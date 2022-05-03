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

rs.seq_mem_limit(0xffff)
rs.seq_mem_write(0x0000, 0x0000, 0x00, 32, "WRITE ADDRESS 0000-0000 (00-1F)")
rs.seq_mem_write(0x0fff, 0x1000, 0x40, 64, "WRITE ADDRESS 0fff-1000 (40-7F)")
rs.seq_mem_write(0x0fff, 0x0fff, 0x80, 64, "WRITE ADDRESS 0fff-0xfff x 2 (80-9F/A0-BF)")
rs.seq_mem_write(0x1fff, 0x1fff, 0xc0, 32, "WRITE ADDRESS 1fff-1fff (C0-DF)")

rs.seq_mem_read(0x0000, 0x0000, 34, "READ ADDRESS 0000-0000")
rs.seq_mem_read(0x0fff, 0x1000, 66, "READ ADDRESS 0fff-1000")
rs.seq_mem_read(0x0fff, 0x0fff, 68, "READ ADDRESS 0fff-0xfff x 2")
#test_mem_read_repeat(0x0fff, 0x0fff, 68, "READ ADDRESS 0fff-0xfff x 2 REPEAT")
test_mem_read_start(0x0fff, 0x1000, 0x1000, 1, 66+34-1, "READ ADDRESS 0fff- CHANGE START(1)")
test_mem_read_start(0x0fff, 0x1000, 0x1000, 10, 66+34-10, "READ ADDRESS 0fff- CHANGE START(10)")
test_mem_read_start(0x0fff, 0x0000, 0x1000, 10, 66+34-10, "READ ADDRESS 0fff- CHANGE START(10/RESET)")
rs.reset()
test_mem_read_stop(0x0fff, 0x0fff, 0x1000, 10, 66+66-10, "READ ADDRESS 0fff- CHANGE STOP")
rs.seq_mem_read(0x1fff, 0x1fff, 34, "READ ADDRESS 1fff-1fff")


rs.msg("READ / WRITE MIX")
rs.reset()
test_mem_read_write(0x0000, 0x0000, 10, 68-10-1, "READ ADDRESS 0000-0000 (10 WRITE)")


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
