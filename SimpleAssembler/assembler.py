import sys # for command line arguments
file_input = sys.argv[1] # input file
file_output = sys.argv[2] # output file
 
# RISC-V encoding format
# [31:25] [24:20] [19:15] [14:12] [11:7] [6:0] Instruction
# funct7 s3 s2 add s1 opcode add
# 0000000 10011 10010 000 01001 0110011

def write_to_bin(bineq): 
    bincode = open(file_output, '+a')
    bincode.write(str(bineq))
    bincode.close()

def ovr_write_to_bin():
    bincode = open(file_output, '+w')
    bincode.close()

def read_instructions(pc): 
    # Retrieves the instruction at the current program counter (pc).
    # Why? - In an assembler, instructions need to be processed sequentially starting from a specific memory address.
    temp = assembly[pc]
    return temp

def opcode(x):
    R_type = ['add', 'sub', 'slt', 'srl', 'or', 'and']
    I_type = ['lw', 'addi', 'jalr']
    S_type = ['sw']
    B_type = ['beq', 'bne', 'blt']
    J_type = ['jal']
    U_type = ['lui', 'auipc']
    
    opc = {
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
    
    if x in opc:
        return opc[x]
    return 'error'

def funct3(x):
    funct3 = {
        # R Type
        'add': '000',
        'sub': '000',
        'slt': '010',
        'srl': '101',
        'or': '110',
        'and': '111',

        # I Type
        'lw': '010',
        'addi': '000',
        'jalr': '000',

        # S Type
        'sw': '010',

        # B Type
        'beq': '000',
        'bne': '001',
        'blt': '100',

        # J Type
        'jal': '000',

        # U Type
        'lui': '000',
        'auipc': '000'
    }
    
    if x in funct3:
        return funct3[x]
    return ''

def funct7(x):
    f7 = {
        'add': '0000000',
        'sub': '0100000',
        'slt': '0000000',
        'srl': '0000000',
        'or': '0000000',
        'and': '0000000'
    }
    
    if x in f7:
        return f7[x]
    return ''

def register_code(x):
    registers_dict={
    'zero': '00000',
    'ra':   '00001',
    'sp':   '00010',
    'gp':   '00011',
    'tp':   '00100',
    't0':   '00101',
    't1':   '00110',
    't2':   '00111',
    's0':   '01000',
    's1':   '01001',
    'a0':   '01010',
    'a1':   '01011',
    'a2':   '01100',
    'a3':   '01101',
    'a4':   '01110',
    'a5':   '01111',
    'a6':   '10000',
    'a7':   '10001',
    's2':   '10010',
    's3':   '10011',
    's4':   '10100',
    's5':   '10101',
    's6':   '10110',
    's7':   '10111',
    's8':   '11000',
    's9':   '11001',
    's10':   '11010',
    's11':   '11011',
    't3':   '11100',
    't4':   '11101',
    't5':   '11110',
    't6':   '11111',
    }
    if x in registers_dict:
        return registers_dict[x]  
    return 'error'
    


def compute_2s_complement(binary_str):
    flipped = ''.join('1' if bit == '0' else '0' for bit in binary_str)
    binary = bin(int(flipped, 2) + 1)[2:]
    return binary.zfill(len(binary_str))
#print(compute_2s_complement('00010111'))

def conversion_to_bits(a):
    if a == 0:
        return "0" 
    bits = []
    while a:
        bits.append(str(a % 2))
        a //= 2
    return ''.join(bits[::-1])
# print(converion_to_bits(256))

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