# div.asm
#
# Expected output: 4

LDI R0,4
LDI R1,1
DIV R0,R1
PRN R0

# Expected output: 1
LDI R0,7
LDI R1,7
DIV R0,R1
PRN R0
HLT