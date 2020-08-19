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
        self.PC = 0 # Program Counter
        self.SP = 7  # Stack Pointer
        self.running = True

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
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


    def run(self):
        """Run the CPU."""
        HLT = 0b00000001 # Halt instruction
        LDI = 0b10000010 # LDI instruction
        PRN = 0b01000111 # PRN instruction
        MUL = 0b10100010 # Multiply instruction
        PUSH = 0b01000101 # Push instruction
        POP = 0b01000110  # Pop instruction

        while self.running:
            instruction_register = self.ram[self.PC]
            reg_a = self.ram[self.PC + 1]
            reg_b = self.ram[self.PC + 2]

            if instruction_register == HLT:
                self.hlt()
            elif instruction_register == LDI:
                self.ldi(reg_a, reg_b)
            elif instruction_register == PRN:
                self.prn(reg_a)
            elif instruction_register == MUL:
                self.mul(reg_a, reg_b)
            elif instruction_register == PUSH:
                self.push(reg_a)
            elif instruction_register == POP:
                self.pop(reg_a)
            else:
                print(f"'{instruction_register}' at address '{self.PC}' not a recognized instruction.")
                self.PC += 1

    def hlt(self):
        """Halt - Exit"""
        self.running = False
        self.PC += 1
        sys.exit(0)

    def ldi(self, reg_a, reg_b):
        """Essentially acts as a pointer"""
        self.reg[reg_a] = reg_b
        self.PC += 3

    def prn(self, reg_a):
        """Prints"""
        print(self.reg[reg_a])
        self.PC += 2

    def mul(self, reg_a, reg_b):
        "Multiplies"
        self.reg[reg_a] *= self.reg[reg_b]
        self.PC += 3

    def push(self, reg_a):
        # Decrease Stack Pointer
        self.SP =- 1
        # Write to RAM.
        self.ram[self.SP] = self.reg[reg_a]
        self.PC += 2
    
    def pop(self, reg_a):
        # Increase Stack Pointer
        self.SP += 1
        # Set Register at reg_a to be the RAM entry of Stack Pointer
        self.reg[reg_a] = self.ram[self.SP]
        self.PC += 2

