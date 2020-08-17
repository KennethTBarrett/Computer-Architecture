"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Memory
        self.ram = [0] * 256
        # Initialize registers
        self.reg = [0] * 8
        # General-Purpose registers
        self.IM = self.reg[5] # Interrupt Mask
        self.IS = self.reg[6] # Interrupt Status 
        self.SP = 0xF4 # Stack Pointer 
        # Special-Purpose Registers
        self.PC = 0 # Program Counter
        self.IR = 0 # Instruction Register
        self.MAR = 0 # Memory Address Register
        self.MDR = 0 # Memory Data Register
        self.FL = 0 # Flag
        self.halt = False

    def ram_read(self, address):
        # Simply return RAM at specified address
        return self.ram[address]
    
    def ram_write(self, address, value):
        # Write value to ram at specified address
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""

        address = 0
        # Open file, set memory address value to integer (instruction, 2 (base))
        with open(program) as file_open:   
            for instruction in file_open:
                instruction = instruction.split('#')[0].strip()
                if instruction == '':
                    continue

                self.ram[address] = int(instruction, 2)

                address += 1 # Increase address location


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001 # Halt instruction handler
        LDI = 0b10000010 # LDI instruction
        PRN = 0b01000111 # PRN instruction
        MUL = 0b10100010 # Multiply instruction
        RET = 0b00010001 # Return
        PUSH = 0b01000101 # Push (Stack)
        POP = 0b01000110  # Pop (Stack)
        CALL = 0b01010000 # Call
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        # Here's a brutal if-else block. TODO: Optimize
        self.halt = False
        while self.halt is False:
            if self.ram[self.PC] == LDI:
                self.reg[self.ram[self.PC + 1]] = self.ram[self.PC + 2]
                self.PC += 3

            elif self.ram[self.PC] == PRN:
                print(self.reg[self.ram[self.PC + 1]])
                self.PC += 2    

            elif self.ram[self.PC] == MUL:      
                self.alu(MUL, self.ram[self.PC + 1], self.ram[self.PC + 2])
                self.PC += 3

            elif self.ram[self.PC] == PUSH: 
                self.push(self.ram[self.PC + 1])

            elif self.ram[self.PC] == POP:
                self.pop(self.ram[self.PC + 1])  

            elif self.ram[self.PC] == CALL: 
                self.call(self.ram_read(self.PC + 1))

            elif self.ram[self.PC] == RET:    
                self.ret() 

            elif self.ram[self.PC] == CMP:      
                self.alu(CMP, self.ram[self.PC + 1], self.ram[self.PC + 2])
                self.PC += 3       

            elif self.ram[self.PC] == JMP:   
                self.jmp(self.ram[self.PC + 1]) 

            elif self.ram[self.PC] == JEQ:   
                self.jeq(self.ram[self.PC + 1])    

            elif self.ram[self.PC] == JNE:   
                self.jne(self.ram[self.PC + 1])           

            elif self.ram[self.PC] == HLT:
                self.hlt()         

            else:
                print('unknown instruction')

    def hlt(self):
        """Halt"""
        self.halt = True
        sys.exit(0)

    def ldi(self, reg_1, reg_2):
        self.reg[reg_1] = self.ram[reg_2]
        self.PC += 3

    def prn(self, reg_1):
        print(self.reg[self.ram[reg_1]])
        self.PC += 2    