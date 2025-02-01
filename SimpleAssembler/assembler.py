import sys # for command line arguments
file_input = sys.argv[1] # input file
file_output = sys.argv[2] # output file
 
# RISC-V encoding format
# [31:25] [24:20] [19:15] [14:12] [11:7] [6:0] Instruction
# funct7 s3 s2 add s1 opcode add
# 0000000 10011 10010 000 01001 0110011

def write_to_bin(bineq): 
    # Writes the binary encoded instruction to the output file.
    # Why? - The assembler needs to store the generated machine code in a binary format 
    # for further execution or testing.
    bincode = open(file_output, '+a')
    bincode.write(str(bineq))
    bincode.close()

def ovr_write_to_bin():
    # Overwrites the output file with an empty content at the start of the process.
    # Why? - This ensures the output file is clean before starting to write the new binary code.
    bincode = open(file_output, '+w')
    bincode.close()

def read_instructions(pc): 
    temp = assembly[pc]
    return temp

def opcode(instype):
    R_type = ['add', 'sub', 'slt', 'srl', 'or', 'and']
    I_type = ['lw', 'addi', 'jalr']
    S_type = ['sw']
    B_type = ['beq', 'bne', 'blt']
    J_type = ['jal']
    U_type = ['lui', 'auipc']
    
    opcodes = {
        # R Type
        'add': '0110011', 
        'sub': '0110011', 
        'slt': '0110011', 
        'and': '0110011',
        'or': '0110011', 
        'srl': '0110011', 

        # I Type
        'lw': '0000011', 
        'addi': '0010011', 
        'jalr': '1100111',

        # S Type
        'sw': '0100011',

        # B Type
        'beq': '1100011', 
        'bne': '1100011', 
        'blt': '1100011', 

        # J Type
        'jal': '1101111',

        # U Type
        'lui': '0110111',
        'auipc': '0010111'
    }
    
    if instype in opcodes:
        return opcodes[instype]
    return 'error'

def funct3(x):
    test = None
    # Determines the funct3 field for certain instruction types (like R-type).
    # Why? - The funct3 helps further define the operation within a given opcode type, 
    # often distinguishing between variations of operations (like add, sub, etc.).
    # lx0 , lx1 , lx2 , lx3 , lx4 , lx5 , lx6 , lx7 , null
    # Logic will be added here to return funct3 value or error

def funct7(x):
    test = None
    # Determines the funct7 field for certain instruction types (like R-type).
    # Why? - The funct7 is used for more complex instruction formats (like shifts or divides), 
    # and helps refine the operation the processor performs.
    # lx0 , lx1 , null
    # Logic will be added here to return funct7 value or error

def register_code(x):
    test = None
    # Converts register names to their corresponding binary representation.
    # Why? - In the RISC-V architecture, registers are represented by 5-bit binary values 
    # to identify the operands in the instruction (e.g., x0 for zero register).
    # If reg = zero then 00000, if reg = ra then 00001, and so on
    # Logic will be added here to convert register names to binary representation

# def complement(a):
#     # Computes the complement of a binary digit.
#     # Why? - Used in two's complement operations, which is essential for handling signed numbers in binary.
#     # If a = 1 then 0, if a = 0 then 1
#     # Logic will be added here to return the complement

# def compute_2s_complement(a):
#     # Computes the two's complement of a given binary string.
#     # Why? - Two's complement is essential for arithmetic operations with negative numbers.
#     # Logic will be added here to return two's complement of the input binary string

# def converion_to_bits(a):
#     # Converts a decimal number to binary.
#     # Why? - Assembly instructions require both immediate values (e.g., offsets) and register values 
#     # to be represented in binary format for proper encoding.
#     # Logic will be added here to convert decimal numbers to binary

def imm(x, opco):
    test = None
    # Converts decimal immediate values into their appropriate binary representation based on the instruction type.
    # Why? - Immediate values are used in instructions like I-type, and need to be converted to binary for encoding.
    # Logic will be added here for converting immediate values to binary

def processor_labels(assembly):
    test = None
    # Processes labels in the assembly code and replaces them with memory addresses or relative offsets.
    # Why? - Labels are used in assembly language for easy references to locations, and 
    # they need to be converted to actual memory addresses or offsets before encoding.
    # Logic will be added here for processing labels and replacing them with addresses

fname = file_input

with open(fname, 'r') as a:
    assembly = [line.strip('\n') for line in a if line.strip()]
assembly = processor_labels(assembly)
ovr_write_to_bin()

# The above part is the main part that includes all the required functions for the assembler.
# the rest of the code will be for bonus part 