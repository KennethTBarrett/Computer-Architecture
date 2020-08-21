# xor.asm
#
# Expected output: 0

LDI R0,1
LDI R1,1
XOR R0,R1
PRN R0

# Expected output: 3
LDI R0,1
LDI R1,2
XOR R0,R1
PRN R0
HLT