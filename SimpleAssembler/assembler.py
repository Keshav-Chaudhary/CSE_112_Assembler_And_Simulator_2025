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
    B = ['beq', 'bne', 'blt', 'bgeu']
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
        'blt': '1100011',
        'bgeu':'1100011'
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
        'blt': '100',
        'bgeu': '111'
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

# def imm(x, opco):
#     num = int(x) # small typo 
#     if opco in ["0000011", "0010011", "1100111"]:
#         bit_length = 12
#         binary = conversion_to_bits(abs(num), bit_length)
#         if num < 0:
#             binary = compute_2s_complement(binary, bit_length)
#         if len(binary) > bit_length:
#             return '-1'
#         return binary

#     elif opco in ["1100011"]:
#         bit_length = 13
#         binary = conversion_to_bits(abs(num), bit_length)
#         if num < 0:
#             binary = compute_2s_complement(binary, bit_length)
#         if len(binary) > bit_length:
#             return '-1'
#         y = binary[0] + binary[2:8]
#         z = binary[8:12] + binary[1]
#         return y, z

#     elif opco in ["0110111", "0010111"]:
#         bit_length = 32
#         binary = conversion_to_bits(abs(num), bit_length)
#         if num < 0:
#             binary = compute_2s_complement(binary, bit_length)
#         if len(binary) > bit_length:
#             return '-1'
#         return binary[:20]

#     elif opco in ["0100011"]:
#         bit_length = 12
#         binary = conversion_to_bits(abs(num), bit_length)
#         if num < 0:
#             binary = compute_2s_complement(binary, bit_length)
#         if len(binary) > bit_length:
#             return '-1'
#         return binary[:7], binary[7:]

#     elif opco in ["1101111"]:
#         bit_length = 21
#         binary = conversion_to_bits(abs(num), bit_length)
#         if num < 0:
#             binary = compute_2s_complement(binary, bit_length)
#         if len(binary) > bit_length:
#             return '-1'
#         binary = binary[0] + binary[10:20] + binary[9] + binary[1:9]
#         return binary


def imm(x, opco):
    num = int(x)
    final = {
        "0000011": 12, "0010011": 12, "1100111": 12,
        "1100011": 13,
        "0110111": 32, "0010111": 32,
        "0100011": 12,
        "1101111": 21
    }

    if opco not in final:
        return 'error'

    bit_length = final[opco]
    binary = conversion_to_bits(abs(num), bit_length)
    if num < 0:
        binary = compute_2s_complement(binary, bit_length)
    if len(binary) > bit_length:
        return 'error'

    if opco in ["0000011", "0010011", "1100111"]:
        return binary

    elif opco == "1100011":
        y = binary[0] + binary[2:8]
        z = binary[8:12] + binary[1]
        return y, z

    elif opco in ["0110111", "0010111"]:
        return binary[:20]

    elif opco == "0100011":
        return binary[:7], binary[7:]

    elif opco == "1101111":
        return binary[0] + binary[10:20] + binary[9] + binary[1:9]


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

fname = file_input

with open(fname, 'r') as a:
    assembly = [line.strip('\n') for line in a if line.strip()]
assembly = processor_labels(assembly)

ovr_write_to_bin()

# The above part is the main fucntions that includes all the required functions for the assembler.
# the rest of the code will be for bonus part and the main logic.

bonus_opcodes = {
    "rst": "1010101",
    "mul": "1010110",
    "halt": "1011101",
    "rvrs": "1011111"
}
cnt = 0
bonus_list = ["mul", "rst", "halt", "rvrs"]
while cnt != len(assembly):
    inst = read_instructions(cnt).split()
    # print('Current Line : ', inst)
    cnt += 1
    
    if inst[0] in ['rst', 'halt']:
        inst = [inst[0]]
    else:
        inst = [inst[0]] + inst[1].split(',')
    
    opco = opcode(inst[0])

    if inst[0] in bonus_list:
        opco = bonus_opcodes.get(inst[0], opco)
    
    # Check if the virtual halt instruction is missing
    if "beq zero,zero,0" not in assembly:
        write_to_bin('Missing Virtual Halt')
        print('Missing Virtual Halt')
        break

    # print(f'Opcode of Instruction {inst[0]} : ', opco)
    # print('Formated Instruction : ', inst)
    # print(opco) #0010011
    # print(repr(opco))
    # print(len(opco))
    # Base Case
    if opco=='error':
        write_to_bin('at line', cnt,'Invalid Instruction Name')
        print('at line', cnt,'Invalid Instruction Name')
        break

    # CASE 1 when opcode is 0010011 and instruction is beq 
    # Instruction beq zero,zero,0
    # output : 00000000000000000000000001100011
    if opco == "1100011" and inst == ['beq', 'zero', 'zero', '0']:
        print("Executed : ", inst)
        try:
            imm_value, imm_type = imm(inst[3], opco)
            reg1_code = register_code(inst[2])
            reg2_code = register_code(inst[1])
            funct3_value = funct3(inst[0])

            bineq = imm_value + reg2_code + reg1_code + funct3_value + imm_type + opco
            
            if 'error' in bineq:
                write_to_bin('at line', cnt, 'Invalid Register Name')
                print(f'at line {cnt} Invalid Register Name')
                break
            elif '-1' in bineq:
                write_to_bin('at line', cnt, 'Invalid Imm Value')
                print(f'at line {cnt} Invalid Imm Value')
                break
            write_to_bin(bineq + ('\n' if cnt != len(assembly) else ''))
            
        except ValueError as e:
            print(f'Invalid Instruction at line {cnt}: {e}')
            break

    # CASE 2 when opcode is 0010011 and instruction is addi 
    # instruction : addi a0,zero,-5
    # output : 11111111101100000000010100010011
    if opco == '0010011':  # Check for a specific opcode
        print("Executed : ", inst)
        # imm_value = imm(inst[3], opco)
        # print("imm_value:", imm_value)
        try:
            # Prepare the binary instruction
            bineq = imm(inst[3], opco) + register_code(inst[2]) + funct3(inst[0]) + register_code(inst[1]) + opco
            # print("immideate value", imm(inst[3], opco))
            # print("register code", register_code(inst[2]))
            # print("funct3", funct3(inst[0]))
            # print("register code", register_code(inst[1]))
            # print("opco", opco)
            # print(bineq)
            
            if 'error' in bineq:
                write_to_bin(f'at line {cnt} Invalid Register Name')
                print(f'at line {cnt} Invalid Register Name')
                break
            elif '-1' in bineq:
                write_to_bin(f'at line {cnt} Invalid Imm Value')
                print(f'at line {cnt} Invalid Imm Value')
                break
            elif cnt == len(assembly):
                write_to_bin(bineq+ ('\n' if cnt != len(assembly) else ''))
            else:
                write_to_bin(bineq+ ('\n' if cnt != len(assembly) else ''))

        except Exception:
            print('Invalid Instruction')
            break
    # To be continued
    
    # CASE 3 when opcode is 0110011 and instructions are in [add,sub,slt,srl,or,and] or .....
    # Instruction : add a0,zero,zero
    # output : 00000000000000000000010100110011
    if opco == '0110011':
        print("Executed : ", inst)
        try:
            reg1_code = register_code(inst[3])
            reg2_code = register_code(inst[2])
            reg3_code = register_code(inst[1])
            funct3_value = funct3(inst[0])
            funct7_value = funct7(inst[0])

            bineq = funct7_value + reg1_code + reg2_code + funct3_value + reg3_code + opco

            if 'error' in bineq:
                write_to_bin('at line', cnt, 'Invalid Register Name')
                print(f'at line {cnt} Invalid Register Name')
                break

            write_to_bin(bineq + ('\n' if cnt != len(assembly) else ''))

        except ValueError as e:
            print(f'Invalid Instruction at line {cnt}: {e}')
            break

    # CASE 4 when opcode is 0000011 and instruction is lw
    # Instruction : lw s2,0(s1)
    # output : 00000000000010010010010100000011
    #print(f"Opcode received: '{opco}'")
    if opco in ['0000011']:
        print("Executed : ", inst)
        try:
            t=inst[2].split('(')
            #print(type(t))
            #print(imm(t[0],opco))
            imm_value = imm(t[0],opco)
            reg1_code = register_code(inst[1])
            reg2_code = register_code(t[1].strip(')'))
            funct3_value = funct3(inst[0])
            bineq = imm_value + reg1_code + reg2_code + funct3_value + opco

            if 'error' in bineq:
                write_to_bin('at line', cnt, 'Invalid Register Name')
                print(f'at line {cnt} Invalid Register Name')
                break
            elif '-1' in bineq:
                write_to_bin('at line', cnt, 'Invalid Imm Value')
                print(f'at line {cnt} Invalid Imm Value')
                break

            write_to_bin(bineq + ('\n' if cnt != len(assembly) else ''))

        except ValueError as e:
            print(f'Invalid Instruction at line {cnt}: {e}')
            break

    # CASE 5 when opcode is 1100111 and instruction is jalr
    # Instruction : jalr s2,s1,16
    # output : 00000001000001001000100101100111
    if opco == '1100111':
        print("Executed : ", inst)
        try:
            #print(inst[0], inst[1], inst[2],inst[3])
            #print(imm_value)
            imm_value = imm(inst[3],opco)
            reg1_code = register_code(inst[2])
            reg2_code = register_code(inst[1]) 
            funct3_value = funct3(inst[0])
            bineq = imm_value + reg1_code + funct3_value + reg2_code + opco
            
            if 'error' in bineq:
                write_to_bin('at line', cnt, 'Invalid Register Name')
                print(f'at line {cnt} Invalid Register Name')
                break
            elif '-1' in bineq:
                write_to_bin('at line', cnt, 'Invalid Imm Value')
                print(f'at line {cnt} Invalid Imm Value')
                break

            write_to_bin(bineq + ('\n' if cnt != len(assembly) else ''))

        except ValueError as e:
            print(f'Invalid Instruction at line {cnt}: {e}')
            break

    # CASE 6 when opcode is 0100011 and instruction are in [sw,sb,sh,sd]
    # Instruction : sw s2,0(s1)
    # output : 00000001001001000010000000100011
    if  opco=='0100011':
        print("Executed : ", inst)
        try:
            t=inst[2].split('(')
            #print(type(t))
            #print(imm(t[0],opco))
            imm_value,imm_type = imm(t[0],opco)
            reg1_code = register_code(inst[1])
            reg2_code = register_code(t[1].strip(')'))
            funct3_value = funct3(inst[0])
            bineq = imm_value + reg1_code + reg2_code + funct3_value + imm_type + opco

            if 'error' in bineq:
                write_to_bin('at line', cnt, 'Invalid Register Name')
                print(f'at line {cnt} Invalid Register Name')
                break
            elif '-1' in bineq:
                write_to_bin('at line', cnt, 'Invalid Imm Value')
                print(f'at line {cnt} Invalid Imm Value')
                break

            write_to_bin(bineq + ('\n' if cnt != len(assembly) else ''))

        except ValueError as e:
            print(f'Invalid Instruction at line {cnt}: {e}')
            break

    # CASE 7 when opcode is 1100011 and instruction are not in ['beq','zero','zero','0']
    # instruction : bgeu s0,s1,96
    # 00000110100101000111000001100011
    if opco in ["1100011"] and inst!=['beq',"zero","zero","0"]:
        print("Executed : ", inst)
        try:
            imm_value,imm_type=imm(inst[3],opco)
            reg1_code = register_code(inst[1])
            reg2_code = register_code(inst[2])
            funct3_value = funct3(inst[0])
            bineq = imm_value + reg2_code + reg1_code + funct3_value + imm_type + opco
            if 'error'in bineq:
                write_to_bin('at line', cnt, 'Invalid Register Name')
                print('at line', cnt, 'Invalid Register Name')
                break
            elif '-1'in bineq:
                write_to_bin('at line',cnt,'Invalid Imm Value')
                print('at line',cnt,'Invalid Imm Value')
                break
            elif cnt==len(assembly):
                write_to_bin(bineq)
            else:
                write_to_bin(bineq + '\n')

        except Exception:
            print('Invalid Instruction')
            break

    # CASE 8 when opcode is 0110111 or 0010111 or 1101111 and instruction are lui , auipc , jal
    if opco in ["0110111","0010111","1101111"]:
        print('Executed : ',inst)
        try:
            imm_value=imm(inst[2],opco)
            reg1_code=register_code(inst[1])
            bineq=imm_value + reg1_code + opco
            if 'error'in bineq:
                write_to_bin('at line', cnt, 'Invalid Register Name')
                print('at line', cnt, 'Invalid Register Name')
                break
            elif '-1'in bineq:
                write_to_bin('at line',cnt,'Invalid Imm Value')
                print('at line',cnt,'Invalid Imm Value')
                break
            elif cnt==len(assembly):
                write_to_bin(bineq)
            else:
                write_to_bin(bineq + '\n')

        except Exception as e:
            print('Invalid Instruction', e) # in case of jal resolve this error : - jal s0,label2
            break
    
    # CASE bonus mul , rst , halt , rvrs
    # when instruction is mul
    if opco == '1010110':
        try:
            bineq = '0000000' + register_code(inst[3])+register_code(inst[2])+ '000'+register_code(inst[1])+opco
            if 'error'in bineq:
                write_to_bin('at line', cnt, 'Invalid Register Name')
                print('at line', cnt, 'Invalid Register Name')
                break
            elif cnt==len(assembly):
                write_to_bin(bineq)
            else:
                write_to_bin(bineq + '\n')
        except Exception:
            print('Invalid Instruction')
            break
    # when instruction is rst
    if opco == '1010101':
        try:
            bineq = '0000000000000000000000000' + opco
            if cnt == len(assembly):
                
                write_to_bin(bineq)
            else:
                write_to_bin(bineq + '\n')
        except Exception:
            print('Invalid Instruction')
            break
    # when instruction is halt
    if opco == '1011101':
        try:
            bineq = '0000000000000000000000000' + opco
            if cnt == len(assembly):
                
                write_to_bin(bineq)
            else:
                write_to_bin(bineq + '\n')
        except Exception:
            print('Invalid Instruction')
            break
    #when instruction is rvrs
    if opco == '1011111':
        try:
            bineq = '000000000000' + register_code(inst[2]) + '000' + register_code(inst[1]) + opco
            if 'error'in bineq:
                write_to_bin('at line', cnt, 'Invalid Register Name')
                print('at line', cnt, 'Invalid Register Name')
                break
            elif cnt==len(assembly):
                write_to_bin(bineq)
            else:
                write_to_bin(bineq + '\n')
        except Exception:
            print('Invalid Instruction')
            break