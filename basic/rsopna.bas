1000 CLEAR ,&HE000
1010 CONSOLE ,,0
1020 OPEN "COM:N81" AS #1
1030 AD0=&HA8:DT0=&HA9
1040 AD1=&HAC:DT1=&HAD
1050 ADDR=&HE000:STAT=&HE000
1060 READ D$
1070 IF D$="FIN" THEN GOTO 1110
1080 POKE ADDR,VAL("&H"+D$): ADDR=ADDR+1
1090 GOTO 1060
1100 '
1110 INPUT #1,C
1120 IF C=1 THEN GOSUB *OPW1
1130 IF C=2 THEN GOSUB *OPR1
1140 IF C=3 THEN GOSUB *OPS1
1150 IF C=4 THEN PRINT #1,""
1160 IF C=5 THEN GOSUB *PAUSE
1170 IF C=6 THEN GOSUB *OPW0
1180 IF C=7 THEN GOSUB *OPR0
1190 IF C=9 THEN GOSUB *STAT
1200 IF C=10 THEN GOSUB *WRM
1210 IF C=11 THEN GOSUB *RDM
1220 IF C=99 THEN GOTO 1250
1230 PRINT #1,"@";
1240 GOTO 1110
1250 END
1260 '
1270 *OPW1
1280 INPUT #1,A$,D$
1290 A=VAL("&H"+A$):D=VAL("&H"+D$)
1300 OUT AD1,A:OUT DT1,D
1310 PRINT #1,"O"+RIGHT$("0"+HEX$(A),2)+":"+RIGHT$("0"+HEX$(D),2)+" ";
1320 RETURN
1330 '
1340 *OPR1
1350 INPUT #1,A$
1360 A=VAL("&H"+A$)
1370 OUT AD1,A:D=INP(DT1)
1380 PRINT #1,"I"+RIGHT$("0"+HEX$(A),2)+":"+RIGHT$("0"+HEX$(D),2)+" ";
1390 RETURN
1400 '
1410 *OPS1
1420 S=INP(AD1)
1430 PRINT #1,"S"+RIGHT$("0"+HEX$(S),2)+"    ";
1440 RETURN
1450 '
1460 *PAUSE
1470 INPUT #1,M$
1480 PRINT #1,""
1490 PRINT #1,M$
1500 CAPS=INP(10) AND 128
1510 'IF CAPS=0 THEN PRINT ELSE INPUT DUMMY$
1520 RETURN
1530 '
1540 *OPW0
1550 INPUT #1,A$,D$
1560 A=VAL("&H"+A$):D=VAL("&H"+D$)
1570 OUT AD0,A:OUT DT0,D
1580 PRINT #1,"o"+RIGHT$("0"+HEX$(A),2)+":"+RIGHT$("0"+HEX$(D),2)+" ";
1590 RETURN
1600 '
1610 *OPR0
1620 INPUT #1,A$
1630 A=VAL("&H"+A$)
1640 OUT AD0,A:D=INP(DT0)
1650 PRINT #1,"i"+RIGHT$("0"+HEX$(A),2)+":"+RIGHT$("0"+HEX$(D),2)+" ";
1660 RETURN
1670 '
1680 *OPS0
1690 S=INP(AD10
1700 PRINT #1,"s"+RIGHT$("0"+HEX$(S),2)+"    ";
1710 RETURN
1720 '
1730 *WRM
1740 INPUT #1,D$
1750 D=VAL("&H"+D$)
1760 INPUT #1,R
1770 FOR I=1 TO R
1780   OUT AD1,&H8:OUT DT1,D
1790   'GOSUB *W
1800   S1=INP(AD1)
1810   OUT AD1,&H10:OUT DT1,&H80
1820   PRINT #1,"W"+RIGHT$("0"+HEX$(D),2)+":"+RIGHT$("0"+HEX$(S1),2);
1830   PRINT #1," ";
1840   D=D+1
1850 NEXT
1860 RETURN
1870 '
1880 *RDM
1890 INPUT #1,R
1900 FOR I=1 TO R
1910   OUT AD1,&H8:D=INP(DT1)
1920   'GOSUB *W
1930   S1=INP(AD1)
1940   OUT AD1,&H10:OUT DT1,&H80
1950   PRINT #1,"R"+RIGHT$("0"+HEX$(D),2)+":"+RIGHT$("0"+HEX$(S1),2);
1960   PRINT #1," ";
1970 NEXT
1980 RETURN
1990 '
2000 *W
2010 FOR WWW=0 TO 3: NEXT: RETURN
2020 '
2030 *STAT
2040 CALL STAT
2041 INPUT #1,D$
2050 RETURN
2060 '
2070 DATA F3,DB,AC,DB,21,E6,02,CA,01,E0,FB,C9,00,00,00,00
2080 DATA F3,06,FF,DB,AC,DB,21,E6,02,20,06,DB,09,A8,C2,13
2090 DATA E0,FB,C9
2100 DATA FIN
-
