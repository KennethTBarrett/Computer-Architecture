"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.RAM = [0] * 256  # Memory
        self.reg = [0] * 8  # Initialize Registers
        self.PC = 0  # Program Counter
        self.SP = 7  # Stack Pointer Index
        self.reg[self.SP] = 0xF4  # Stack Pointer Register
        self.FL = False  # Flag
        self.running = True
        # Instructions
        self.instructions = {
                                'LDI': 0b10000010,
                                'PRN': 0b01000111,
                                'HLT': 0b00000001,
                                'MUL': 0b10100010,
                                'ADD':  0b10100000,
                                'PUSH': 0b01000101,
                                'POP': 0b01000110,
                                'CALL': 0b01010000,
                                'RET': 0b00010001,
                                'NOP': 0b00000000,
                                'JLE': 0b01011001,
                                'JGE': 0b01011010,
                                'DIV': 0b10100011,
                                'SUB': 0b10100001,
                                'CMP': 0b10100111,
                                'JMP': 0b01010100,
                                'JEQ': 0b01010101,
                                'JNE': 0b01010110,
                                'AND': 0b10101000,
                                'OR': 0b10101010,
                                'XOR': 0b10101011,
                                'MOD': 0b10100100
                            }

    def ram_read(self, address):
        """Returns information stored in RAM at specified address."""
        return self.RAM[address]

    def ram_write(self, address, value):
        """Writes a value to RAM using specified address."""
        self.RAM[address] = value

    def load(self, program):
        """Load program into memory."""
        address = 0

        # Open file, split instructions.
        with open(program) as file_open:
            for instruction in file_open:
                instruction = instruction.split('#')[0].strip()
                if instruction == '':
                    continue
                # Set memory address value to integer (instruction, 2 (base))
                self.ram_write(address, int(instruction, 2))
                address += 1  # Increase address location

    def get_key(self, value):
        """Helper function to get the instruction key based upon its
        value in the register."""
        for key, val in self.instructions.items():
            if val == value:
                return(key)

    def run(self):
        """Run the CPU."""
        instructions = self.instructions
        # This will be used later for ease in using our ALU.
        alu_instructions = {op: instructions.get(op) for op in
                            ["ADD", "AND", "CMP", "DIV",
                             "MOD", "MUL", "OR", "SUB", "XOR"]}
        # Non-ALU Operations.
        not_alu = {op: instructions.get(op) for op in instructions
                   if op not in alu_instructions.keys()}

        while self.running:
            # Define our instruction register.
            instruction_register = self.ram_read(self.PC)

            # Handles ALU operations.
            if instruction_register in alu_instructions.values():
                reg_a = self.ram_read(self.PC + 1)
                reg_b = self.ram_read(self.PC + 2)
                # Get the operation returned from our helper function.
                op = self.get_key(instruction_register)
                # Call ALU.
                self.alu(op, reg_a, reg_b)

            # Handles all non-ALU operations.
            elif instruction_register in not_alu.values():
                # Get the specified key returned from helper function.
                operation_key = self.get_key(instruction_register)
                # This will allow us to use our operation key.
                operation = getattr(self, operation_key)
                operation()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # Multiplication operation.
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.PC += 3

        # Addition operation.
        elif op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.PC += 3

        # Division operation.
        elif op == "DIV":
            if self.reg[reg_b] == 0:
                raise Exception("Cannot divide by 0!")
            else:
                self.reg[reg_a] /= self.reg[reg_b]
                self.PC += 3

        # Subtraction operation.
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.PC += 3

        # Comparison operation.
        elif op == "CMP":
            # Equal-To
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = '0000000E'
            # Less-Than
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = '00000L00'
            # Less-Than or Equal-To
            elif self.reg[reg_a] <= self.reg[reg_b]:
                self.FL = '00000L0E'
            # Greater-Than
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = '000000G0'
            # Greater-Than or Equal-To
            elif self.reg[reg_a] >= self.reg[reg_b]:
                self.FL = '000000GE'
            self.PC += 3

        # Modulo operation.
        elif op == "MOD":
            if self.reg[reg_b] == 0:
                raise Exception("Cannot mod by value of 0.")
            else:
                self.reg[reg_a] %= self.reg[reg_b]
            self.PC += 3

        # And operation.
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
            self.PC += 3

        # Or operation.
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
            self.PC += 3

        # Exclusive-Or operation.
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
            self.PC += 3

        # If ALU Operation Unsupported, raise Exception.
        else:
            raise Exception("Unsupported ALU operation")

    def CALL(self):
        # Decrease Stack Pointer
        self.reg[self.SP] -= 1
        # Next instruction for after current subroutine complete.
        next_instruction = self.PC + 2
        # Put that address on stack.
        self.ram_write(self.reg[self.SP], next_instruction)
        # Set PC to register calling from/address within.
        self.PC = self.reg[self.ram_read(self.PC + 1)]

    def RET(self):
        # Set PC to address at top of stack.
        self.PC = self.ram_read(self.reg[self.SP])
        # Increase Stack Pointer.
        self.reg[self.SP] += 1

    def LDI(self):
        # Get appropriate register index.
        reg_index = self.ram_read(self.PC + 1)
        # Set that index to be PC + 2 in RAM.
        self.reg[reg_index] = self.ram_read(self.PC + 2)
        self.PC += 3

    def PUSH(self):
        # Decrease stack pointer.
        self.reg[self.SP] -= 1
        to_push = self.reg[self.ram_read(self.PC + 1)]
        # Copy to memory.
        self.ram_write(self.reg[self.SP], to_push)
        self.PC += 2

    def POP(self):
        # Item to pop (at stack pointer)
        item_pop = self.ram_read(self.reg[self.SP])
        # Find register, copy into it.
        reg_to_pop = self.ram_read(self.PC + 1)
        self.reg[reg_to_pop] = item_pop
        # Increase stack pointer to new position.
        self.reg[self.SP] += 1
        self.PC += 2

    def PRN(self):
        # Print.
        print(self.reg[self.ram_read(self.PC + 1)])
        self.PC += 2

    def HLT(self):
        # Stop running, exit.
        self.running = False
        self.PC += 1
        sys.exit(0)

    def JMP(self):
        # Register to jump to.
        jump_reg = self.ram_read(self.PC + 1)
        # Set PC to that address.
        self.PC = self.reg[jump_reg]

    def JEQ(self):
        # Make jump if flag is equals.
        if self.FL == '0000000E':
            jump_reg = self.ram_read(self.PC + 1)
            self.PC = self.reg[jump_reg]
        else:
            self.PC += 2

    def JNE(self):
        # Same as JEQ but jump if flag != Equals.
        if self.FL != '0000000E':
            jump_reg = self.ram_read(self.PC + 1)
            self.PC = self.reg[jump_reg]
        else:
            self.PC += 2

    def JLE(self):
        # Make jump if flag is less than or equal to.
        if self.FL == '00000L0E':
            jump_reg = self.ram_read(self.PC + 1)
            self.PC = self.reg[jump_reg]
        else:
            self.PC += 2

    def JGE(self):
        # Make jump if flag is greater than or equal to.
        if self.FL == '000000GE':
            jump_reg = self.ram_read(self.PC + 1)
            self.PC = self.reg[jump_reg]
        else:
            self.PC += 2

    def NOP(self):
        # Simply increases program counter (does nothing).
        self.PC += 1
