import RsOPNA
import time

def mem_init(start, stop, count, msg):
    rs.msg(msg)
    rs.out(0x10, 0x08).out(0x10, 0x80)
    rs.out(0x00, 0x30).out(0x01, 0x02)
    rs.out(0x02, start & 0xff).out(0x03, (start >> 8) & 0xff)
    rs.out(0x04, stop & 0xff).out(0x05, (stop >> 8) & 0xff)
    rs.nl()
    rs.mrd(count).nl()
    rs.out(0x00, 0x00).out(0x10, 0x80).nl()

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

rs.seq_mem_limit(0xffff)
rs.seq_mem_fill(0x0000, 0x000f, 0x80, 32 * 0x10, "FILL 0000-000f (80)")
rs.seq_mem_fill_random(0x0010, 0x001f, 32 * 0x10, "FILL 0010-001f (RND)")
rs.seq_play(0x0010, 0x001f, 4719, 0xff, True, "PLAY")

for i in range(10):
    rs.stat()
    time.sleep(1)

rs.seq_stop("STOP")
