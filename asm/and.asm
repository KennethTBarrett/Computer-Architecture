# and.asm
#
# Expected output: 0

LDI R0,3
LDI R1,4
AND R0,R1
PRN R0

# Expected output: 7
LDI R0,7
LDI R1,7
AND R0,R1
PRN R0
HLT