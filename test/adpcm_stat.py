import RsOPNA

def test_stat_read(rs, rec, memdata, repeat):
    control1=(rec<<6) | (memdata<<5) | (repeat<<4)
    rs.msg("READ: REC={:d} / MEMDATA={:d} / REPEAT={:d}".format(rec, memdata, repeat))
    rs.reset()
    rs.stat().nl()
    rs.out(0x10, 0x80).stat().nl()
    rs.out(0x00, control1).stat().nl()

    for i in range(4):
        rs.out(0x10, 0x80).stat().nl()
        rs.inp(0x08).stat().nl()

def test_stat_write(rs, rec, memdata, repeat):
    control1=(rec<<6) | (memdata<<5) | (repeat<<4)
    rs.msg("WRITE: REC={:d} / MEMDATA={:d} / REPEAT={:d}".format(rec, memdata, repeat))
    rs.reset()
    rs.out(0x10, 0x80).stat().nl()
    rs.out(0x00, control1).stat().nl()

    for i in range(4):
        rs.out(0x10, 0x80).stat().nl()
        rs.out(0x08, 0x00).stat().nl()

pat= [
    0x00, 0x00,
    0x00, 0x00,
    0x00, 0xcb,
    0x00, 0x00,

    0x00, 0x00,
    0x00, 0x00,
    0x00, 0xcb,
    0x00, 0x00,

    0x00, 0x00,
    0x00, 0x00,
    0x00, 0xcb,
    0x00, 0x00,

    0x00, 0x00,
    0x00, 0x00,
    0x00, 0xcb,
    0x00, 0x00,
]

rs = RsOPNA.RsOPNA()
rs.open()

rs.stat().nl()
rs.out(0x10, 0x00).stat().nl()
rs.out(0x10, 0x80).stat().nl()
rs.out(0x10, 0x00).stat().nl()

rs.reset()
rs.stat().nl()

rs.seq_mem_fill_pat(0, 0, pat, 32, "FILL INITIAL DATA")

rs.out(0x01, 0x02).stat().nl()

rs.out(0x02, 0x00).out(0x03, 0x00).stat().nl()
rs.out(0x04, 0x00).out(0x05, 0x00).stat().nl()


test_stat_read(rs, 0, 0, 0)
test_stat_read(rs, 0, 1, 0)
test_stat_read(rs, 1, 0, 0)
test_stat_read(rs, 1, 1, 0)
test_stat_read(rs, 0, 0, 1)
test_stat_read(rs, 0, 1, 1)
test_stat_read(rs, 1, 0, 1)
test_stat_read(rs, 1, 1, 1)

test_stat_write(rs, 0, 0, 0)
test_stat_write(rs, 0, 1, 0)
test_stat_write(rs, 1, 0, 0)
test_stat_write(rs, 1, 1, 0)
test_stat_write(rs, 0, 0, 1)
test_stat_write(rs, 0, 1, 1)
test_stat_write(rs, 1, 0, 1)
test_stat_write(rs, 1, 1, 1)

"""
Run after Power On
------------------------

S00    
O10:00 S08    
O10:80 S08    
O10:00 S08    
O00:01 O00:00 
S08    

FILL INITIAL DATA
O10:00 O10:80 O00:60 O01:02 O02:00 O03:00 O04:00 O05:00 

00000 O08:00 O08:00 O08:00 O08:00 O08:00 O08:CB O08:00 O08:00 O08:00 O08:00 O08:00 O08:00 O08:00 O08:CB O08:00 O08:00 
00010 O08:00 O08:00 O08:00 O08:00 O08:00 O08:CB O08:00 O08:00 O08:00 O08:00 O08:00 O08:00 O08:00 O08:CB O08:00 O08:00 O00:00 O10:80 
O01:02 S08    
O02:00 O03:00 S08    
O04:00 O05:00 S08    

READ: REC=0 / MEMDATA=0 / REPEAT=0
O00:01 O00:00 
S08    
O10:80 S08    
O00:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    

READ: REC=0 / MEMDATA=1 / REPEAT=0
O00:01 O00:00 
S08    
O10:80 S08    
O00:20 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    

READ: REC=1 / MEMDATA=0 / REPEAT=0
O00:01 O00:00 
S0C    
O10:80 S08    
O00:40 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    

READ: REC=1 / MEMDATA=1 / REPEAT=0
O00:01 O00:00 
S08    
O10:80 S08    
O00:60 S08    
O10:80 S08    
I08:00 S08    
O10:80 S00    
I08:00 S00    
O10:80 S00    
I08:00 S00    
O10:80 S00    
I08:00 S00    

READ: REC=0 / MEMDATA=0 / REPEAT=1
O00:01 O00:00 
S08    
O10:80 S08    
O00:10 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    

READ: REC=0 / MEMDATA=1 / REPEAT=1
O00:01 O00:00 
S08    
O10:80 S08    
O00:30 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    

READ: REC=1 / MEMDATA=0 / REPEAT=1
O00:01 O00:00 
S0C    
O10:80 S08    
O00:50 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    
O10:80 S08    
I08:00 S08    

READ: REC=1 / MEMDATA=1 / REPEAT=1
O00:01 O00:00 
S08    
O10:80 S08    
O00:70 S08    
O10:80 S08    
I08:00 S08    
O10:80 S00    
I08:00 S00    
O10:80 S00    
I08:00 S00    
O10:80 S00    
I08:00 S00    

WRITE: REC=0 / MEMDATA=0 / REPEAT=0
O00:01 O00:00 
O10:80 S08    
O00:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    

WRITE: REC=0 / MEMDATA=1 / REPEAT=0
O00:01 O00:00 
O10:80 S08    
O00:20 S08    
O10:80 S08    
O08:00 S08    
O10:80 S00    
O08:00 S00    
O10:80 S00    
O08:00 S00    
O10:80 S00    
O08:00 S00    

WRITE: REC=1 / MEMDATA=0 / REPEAT=0
O00:01 O00:00 
O10:80 S08    
O00:40 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    

WRITE: REC=1 / MEMDATA=1 / REPEAT=0
O00:01 O00:00 
O10:80 S08    
O00:60 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    

WRITE: REC=0 / MEMDATA=0 / REPEAT=1
O00:01 O00:00 
O10:80 S08    
O00:10 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    

WRITE: REC=0 / MEMDATA=1 / REPEAT=1
O00:01 O00:00 
O10:80 S08    
O00:30 S08    
O10:80 S08    
O08:00 S08    
O10:80 S00    
O08:00 S00    
O10:80 S00    
O08:00 S00    
O10:80 S00    
O08:00 S00    

WRITE: REC=1 / MEMDATA=0 / REPEAT=1
O00:01 O00:00 
O10:80 S08    
O00:50 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    

WRITE: REC=1 / MEMDATA=1 / REPEAT=1
O00:01 O00:00 
O10:80 S08    
O00:70 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
O10:80 S08    
O08:00 S08    
"""