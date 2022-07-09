import RsOPNA

'''
DRAM EXISTING CHECK register accsss sequence by METAL FORCE (PC-98)
'''

rs = RsOPNA.RsOPNA()
rs.open()
rs.reset()

# --------------------------------
rs.msg("WRITE TEST DATA").nl()
# --------------------------------

# FLAG CONTROL
rs.stat().nl()
rs.out(0x10, 0x00).nl()
rs.stat().nl()
rs.out(0x10, 0x80).nl()

# CONTROL 1
rs.stat().nl()
rs.out(0x00, 0x60).nl()

# CONTROL 2
rs.stat().nl()
rs.out(0x01, 0x02).nl()

# START ADDRESS
rs.stat().nl()
rs.out(0x02, 0xff).nl()
rs.stat().nl()
rs.out(0x03, 0x1f).nl()

# STOP ADDRESS
rs.stat().nl()
rs.out(0x04, 0xff).nl()
rs.stat().nl()
rs.out(0x05, 0x1f).nl()

# LIMIT ADDRESS
rs.stat().nl()
rs.out(0x0c, 0xff).nl()
rs.stat().nl()
rs.out(0x0d, 0xff).nl()

for i in range(32):
    rs.out(0x08, 0x30 + i)
    rs.stat().nl()

# CONTROL 1
rs.stat().nl()
rs.out(0x00, 0x00).nl()

# FLAG CONTROL
rs.stat().nl()
rs.out(0x10, 0x80).nl()


# --------------------------------
rs.msg("READ TEST DATA").nl()
# --------------------------------

# FLAG CONTROL
rs.stat().nl()
rs.out(0x10, 0x00).nl()
rs.stat().nl()
rs.out(0x10, 0x80).nl()

# CONTROL 1
rs.stat().nl()
rs.out(0x00, 0x20).nl()

# CONTROL 2
rs.stat().nl()
rs.out(0x01, 0x02).nl()

# START ADDRESS
rs.stat().nl()
rs.out(0x02, 0xff).nl()
rs.stat().nl()
rs.out(0x03, 0x1f).nl()

# STOP ADDRESS
rs.stat().nl()
rs.out(0x04, 0xff).nl()
rs.stat().nl()
rs.out(0x05, 0x1f).nl()

# LIMIT ADDRESS
rs.stat().nl()
rs.out(0x0c, 0xff).nl()
rs.stat().nl()
rs.out(0x0d, 0xff).nl()

for i in range(32 + 2):
    rs.inp(0x08)
    rs.stat()
    rs.out(0x10, 0x80)
    rs.stat().nl()

# CONTROL 1
rs.stat().nl()
rs.out(0x00, 0x00).nl()

# FLAG CONTROL
rs.stat().nl()
rs.out(0x10, 0x80).nl()


'''
----------------------------------------------------------------
reference log from YM2608 on PC-8801mkIISR with SB2(PC-8801-23)
  O : write register (A1=1)
  I : read register (A1=1)
  S : read status1
----------------------------------------------------------------


O00:01 O00:00 

WRITE TEST DATA

S08    
O10:00 
S08    
O10:80 
S08    
O00:60 
S08    
O01:02 
S08    
O02:FF 
S08    
O03:1F 
S08    
O04:FF 
S08    
O05:1F 
S08    
O0C:FF 
S08    
O0D:FF 
O08:30 S08    
O08:31 S08    
O08:32 S08    
O08:33 S08    
O08:34 S08    
O08:35 S08    
O08:36 S08    
O08:37 S08    
O08:38 S08    
O08:39 S08    
O08:3A S08    
O08:3B S08    
O08:3C S08    
O08:3D S08    
O08:3E S08    
O08:3F S08    
O08:40 S08    
O08:41 S08    
O08:42 S08    
O08:43 S08    
O08:44 S08    
O08:45 S08    
O08:46 S08    
O08:47 S08    
O08:48 S08    
O08:49 S08    
O08:4A S08    
O08:4B S08    
O08:4C S08    
O08:4D S08    
O08:4E S08    
O08:4F S0C    
S0C    
O00:00 
S0C    
O10:80 

READ TEST DATA

S08    
O10:00 
S08    
O10:80 
S08    
O00:20 
S08    
O01:02 
S08    
O02:FF 
S08    
O03:1F 
S08    
O04:FF 
S08    
O05:1F 
S08    
O0C:FF 
S08    
O0D:FF 
I08:4F S48    O10:80 S48    
I08:4F S48    O10:80 S48    
I08:30 S08    O10:80 S08    
I08:31 S08    O10:80 S08    
I08:32 S08    O10:80 S08    
I08:33 S08    O10:80 S08    
I08:34 S08    O10:80 S08    
I08:35 S08    O10:80 S08    
I08:36 S08    O10:80 S08    
I08:37 S08    O10:80 S08    
I08:38 S08    O10:80 S08    
I08:39 S08    O10:80 S08    
I08:3A S08    O10:80 S08    
I08:3B S08    O10:80 S08    
I08:3C S08    O10:80 S08    
I08:3D S08    O10:80 S08    
I08:3E S08    O10:80 S08    
I08:3F S08    O10:80 S08    
I08:40 S48    O10:80 S48    
I08:41 S48    O10:80 S48    
I08:42 S48    O10:80 S48    
I08:43 S48    O10:80 S48    
I08:44 S48    O10:80 S48    
I08:45 S48    O10:80 S48    
I08:46 S48    O10:80 S48    
I08:47 S48    O10:80 S48    
I08:48 S48    O10:80 S08    
I08:49 S48    O10:80 S48    
I08:4A S48    O10:80 S48    
I08:4B S48    O10:80 S48    
I08:4C S48    O10:80 S08    
I08:4D S48    O10:80 S48    
I08:4E S48    O10:80 S40    
I08:4F S4C    O10:80 S48    
S08    
O00:00 
S08    
O10:80 
'''
