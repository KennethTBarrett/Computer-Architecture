# or.asm
#
# Expected output: 1

LDI R0,1
LDI R1,1
OR R0,R1
PRN R0

# Expected output: 3
LDI R0,1
LDI R1,2
OR R0,R1
PRN R0
HLT