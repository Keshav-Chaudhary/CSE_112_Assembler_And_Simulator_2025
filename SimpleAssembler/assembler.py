import sys # for command line arguments
import re
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
    temp = assembly[pc]
    return temp

def opcode(x):
    R = ['add', 'sub', 'slt', 'srl', 'or', 'and']
    I = ['lw', 'addi', 'jalr']
    S = ['sw']
    B = ['beq', 'bne', 'blt']
    J = ['jal']
    U = ['lui', 'auipc']
    
    R_opc = {
        'add': '0110011', 
        'sub': '0110011', 
        'slt': '0110011', 
        'and': '0110011',
        'or': '0110011', 
        'srl': '0110011'
    }

    I_opc = {
        'lw': '0000011', 
        'addi': '0010011', 
        'jalr': '1100111'
    }

    S_opc = {
        'sw': '0100011'
    }

    B_opc = {
        'beq': '1100011', 
        'bne': '1100011', 
        'blt': '1100011'
    }

    J_opc = {
        'jal': '1101111'
    }

    U_opc = {
        'lui': '0110111',
        'auipc': '0010111'
    }

    if x in R:
        return R_opc[x]
    elif x in I:
        return I_opc[x]
    elif x in S:
        return S_opc[x]
    elif x in B:
        return B_opc[x]
    elif x in J:
        return J_opc[x]
    elif x in U:
        return U_opc[x]
    else:
        return 'error'

# def test_opcode():
#     assert opcode('add') == '0110011'
#     assert opcode('lw') == '0000011'
#     assert opcode('invalid') == 'error'

def funct3(x):
    r_type = {
        'add': '000',
        'sub': '000',
        'slt': '010',
        'srl': '101',
        'or': '110',
        'and': '111'
    }

    i_type = {
        'lw': '010',
        'addi': '000',
        'jalr': '000'
    }

    s_type = {
        'sw': '010'
    }

    b_type = {
        'beq': '000',
        'bne': '001',
        'blt': '100'
    }

    j_type = {
        'jal': '000'
    }

    u_type = {
        'lui': '000',
        'auipc': '000'
    }

    if x in r_type:
        return r_type[x]
    elif x in i_type:
        return i_type[x]
    elif x in s_type:
        return s_type[x]
    elif x in b_type:
        return b_type[x]
    elif x in j_type:
        return j_type[x]
    elif x in u_type:
        return u_type[x]
    return 'error'

# def test_funct3():
#     assert funct3('add') == '000'
#     assert funct3('lw') == '010'
#     assert funct3('abcde') == ''

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
    return 'error'

# def test_funct7():
#     assert funct7('add') == '0000000'
#     assert funct7('sub') == '0100000'
#     assert funct7('invalid') == ''

# test_opcode()
# test_funct3()
# test_funct7()

def register_code(x):
    registers_dict={
    'zero': '00000',
    'ra':   '00001',
    'sp':   '00010',
    'gp':   '00011',
    'tp':   '00100',
    't0':   '00101', 't1':   '00110', 't2':   '00111',
    's0':   '01000', 's1':   '01001', 's2':   '10010', 's3':   '10011', 's4':   '10100', 's5':   '10101',
    's6':   '10110', 's7':   '10111', 's8':   '11000', 's9':   '11001', 's10':   '11010', 's11':   '11011',
    'a0':   '01010', 'a1':   '01011', 'a2':   '01100', 'a3':   '01101', 'a4':   '01110', 'a5':   '01111', 'a6':   '10000', 'a7':   '10001',
    't3':   '11100', 't4':   '11101', 't5':   '11110', 't6':   '11111',
    }
    if x in registers_dict:
        return registers_dict[x]  
    return 'error'
#print(register_code('s9'))  


def compute_2s_complement(binary_str, length):
    flipped = ''.join('1' if bit == '0' else '0' for bit in binary_str)
    binary = bin(int(flipped, 2) + 1)[2:] 
    return binary.zfill(length)
#print(compute_2s_complement((conversion_to_bits(256,12)),10))

def conversion_to_bits(num, length):
    if num == 0:
        return "0" * length 
    bits = []
    while num:
        bits.append(str(num % 2))
        num //= 2
    
    binary_str = ''.join(bits[::-1])
    if len(binary_str) < length:
        binary_str = binary_str.rjust(length, '0')
    elif len(binary_str) > length:
        binary_str = binary_str[-length:]
    return binary_str
# print(converion_to_bits(256,12))

def imm(x, opco):
    num = int(num)
    if opco in ["0000011", "0010011", "1100111"]:
        bit_length = 12
        binary = conversion_to_bits(abs(num), bit_length)
        if num < 0:
            binary = compute_2s_complement(binary, bit_length)
        if len(binary) > bit_length:
            return '-1'
        return binary

    elif opco in ["1100011"]:
        bit_length = 13
        binary = conversion_to_bits(abs(num), bit_length)
        if num < 0:
            binary = compute_2s_complement(binary, bit_length)
        if len(binary) > bit_length:
            return '-1'
        y = binary[0] + binary[2:8]
        z = binary[8:12] + binary[1]
        return y, z

    elif opco in ["0110111", "0010111"]:
        bit_length = 32
        binary = conversion_to_bits(abs(num), bit_length)
        if num < 0:
            binary = compute_2s_complement(binary, bit_length)
        if len(binary) > bit_length:
            return '-1'
        return binary[:20]

    elif opco in ["0100011"]:
        bit_length = 12
        binary = conversion_to_bits(abs(num), bit_length)
        if num < 0:
            binary = compute_2s_complement(binary, bit_length)
        if len(binary) > bit_length:
            return '-1'
        return binary[:7], binary[7:]

    elif opco in ["1101111"]:
        bit_length = 21
        binary = conversion_to_bits(abs(num), bit_length)
        if num < 0:
            binary = compute_2s_complement(binary, bit_length)
        if len(binary) > bit_length:
            return '-1'
        binary = binary[0] + binary[10:20] + binary[9] + binary[1:9]
        return binary
#print(imm(5, '1101111'))
#print(imm(3, '1100011'))
#print(imm(5, '0110111'))
#print(imm(5, '0100011'))
#print(imm(5, '1101111'))


def processor_labels(assembly):
    label_dict = {}
    
    for i in range(len(assembly)):
        assembly[i] = assembly[i].lstrip() 
        
        match = re.match(r'(\w+):\s*(.*)', assembly[i])
        if match:
            label_dict[match.group(1)] = i * 4
            assembly[i] = match.group(2)

        for label, address in label_dict.items():
            if label in assembly[i]:
                assembly[i] = assembly[i].replace(label, str(address - (i * 4)))

    return assembly
# assembly1 = [
#     "label1: ADD R1, R2, R3",
#     "SUB R4, R5, R6",
#     "label2: MUL R7, R8, R9",
#     "BEQ R1, R2, label1"
# ]
# expected1 =['ADD R1, R2, R3', 'SUB R4, R5, R6', 'MUL R7, R8, R9', 'BEQ R1, R2, -12']
# print(processor_labels(assembly1)==expected1) -- > True 
def logic(opco, inst, count):

    if opco in ['0010011']:
        # imm_value = imm(inst[3], opco)
        print("imm_value:", imm(inst[3], opco)) #bekaar mein memory waste ho rahi thi variable banane se

        try:
            bineq = imm(inst[3],opco) + register_code(inst[2]) + funct3(inst[0]) + register_code(inst[1]) + opco
            
            if 'error' in bineq or '-1' in bineq: #error print hojaata agar hota toh isse badiya pehele check karlo
                error_message = f'at line {count} Invalid Register Name'
                write_to_bin(error_message)
                print(error_message)
                break
            # elif '-1' in bineq:                                           #ye bhi error print karne ke liye tha same code toh join kardis
            #     error_message = f'at line {count} Invalid Imm Value'
            #     write_to_bin(error_message)
            #     print(error_message)
            #     break

            print("immideate value",imm(inst[3],opco))
            print("register code",register_code(inst[2]))
            print("funct3",funct3(inst[0]))
            print("register code",register_code(inst[1]))
            print("opco",opco)
            print(bineq)

            write_to_bin(bineq + ('\n' if count < len(assembly) else '')) #if else ek hi line mein likhdis
        except Exception as e:
            # print('Invalid Instruction')
            print(e) #abhi error ke liye hai baadmein comment kar dena aur upar wala print uncomment kar dena
            break

    elif opco in ["0000011"]:
        # imm_value = imm(inst[3], opco)
        print("imm_value:", imm(inst[3], opco))

        try:
            bineq = imm(inst[3],opco) + register_code(inst[2]) + funct3(inst[0]) + register_code(inst[1]) + opco
            
            if 'error' in bineq or '-1' in bineq:
                error_message = f'at line {count} Invalid Register Name'
                write_to_bin(error_message)
                print(error_message)
                break
            # elif '-1' in bineq:
            #     error_message = f'at line {count} Invalid Imm Value'
            #     write_to_bin(error_message)
            #     print(error_message)
            #     break

            print("immideate value",imm(inst[3],opco))
            print("register code",register_code(inst[2]))
            print("funct3",funct3(inst[0]))
            print("register code",register_code(inst[1]))
            print("opco",opco)
            print(bineq)

            write_to_bin(bineq + ('\n' if count < len(assembly) else ''))
        except Exception as e:
            # print('Invalid Instruction')
            print(e)
            break
    
    elif opco in ['1100111']:
        # imm_value = imm(inst[3], opco)
        print("imm_value:", imm(inst[3], opco))

        try:
            bineq = imm(inst[3],opco) + register_code(inst[2]) + funct3(inst[0]) + register_code(inst[1]) + opco
            
            if 'error' in bineq or '-1' in bineq:
                error_message = f'at line {count} Invalid Register Name'
                write_to_bin(error_message)
                print(error_message)
                break
            # elif '-1' in bineq:
            #     error_message = f'at line {count} Invalid Imm Value'
            #     write_to_bin(error_message)
            #     print(error_message)
            #     break

            print("immideate value",imm(inst[3],opco))
            print("register code",register_code(inst[2]))
            print("funct3",funct3(inst[0]))
            print("register code",register_code(inst[1]))
            print("opco",opco)
            print(bineq)

            write_to_bin(bineq + ('\n' if count < len(assembly) else ''))
        except Exception as e:
            # print('Invalid Instruction')
            print(e)
            break


fname = file_input

with open(fname, 'r') as a:
    assembly = [line.strip('\n') for line in a if line.strip()]
assembly = processor_labels(assembly)

ovr_write_to_bin()

# The above part is the main fucntions that includes all the required functions for the assembler.
# the rest of the code will be for bonus part and the main logic.

