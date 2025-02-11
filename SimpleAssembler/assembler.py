import sys # for command line arguments
# import re
file_input = sys.argv[1] # Input file containing assembly code
file_output = sys.argv[2]  # Output file to store binary machine code
# RISC-V encoding format
# [31:25] [24:20] [19:15] [14:12] [11:7] [6:0] Instruction
# funct7 s3 s2 add s1 opcode add
# 0000000 10011 10010 000 01001 0110011

def write_to_bin(bineq):
    """
    Appends binary code to the output file.
    Args:
        bineq (str): Binary string to write to the file.
    """ 
    bincode = open(file_output, '+a')
    bincode.write(str(bineq))
    bincode.close()

def ovr_write_to_bin():
    """
    Clears the output file before writing new binary code.
    """
    bincode = open(file_output, '+w')
    bincode.close()

def read_instructions(pc): 
    """
    Reads an instruction from the assembly code at the given program counter (PC).
    Args:
        pc (int): Program counter (index of the instruction in the assembly list).
    Returns:
        str: The instruction at the specified PC.
    """
    temp = assembly[pc]
    return temp

def opcode(x):
    """
    Returns the opcode for a given instruction.
    Args:
        x (str): Instruction name (e.g., "add", "lw").
    Returns:
        str: Corresponding opcode.
    """
    R = ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]
    I1 = ["lw"]
    I2 = ["addi", "sltiu"]
    I3 = ["jalr"]
    S = ["sw", "sb", "sh", "sd"]
    B = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
    U1 = ["lui"]
    U2 = ["auipc"]
    J = ["jal"]

    op = {
        # R-Type
        "add": "0110011", "sub": "0110011", "sll": "0110011", "slt": "0110011", "sltu": "0110011", "xor": "0110011", "srl": "0110011", "or": "0110011", "and": "0110011",
        # I-Type
        "lw": "0000011",
        # I-Type
        "addi": "0010011", "sltiu": "0010011",
        # I-Type
        "jalr": "1100111",
        # S-Type
        "sw": "0100011", "sb": "0100011", "sh": "0100011", "sd": "0100011",
        # B-Type
        "beq": "1100011", "bne": "1100011", "blt": "1100011", "bge": "1100011", "bltu": "1100011", "bgeu": "1100011",
        # U-Type
        "lui": "0110111",
        # U-Type
        "auipc": "0010111",
        # J-Type
        "jal": "1101111"
    }

    return op.get(x, 'error')

def funct3(x):
    """
    Returns the funct3 code for a given instruction.
    Args:
        x (str): Instruction name.
    Returns:
        str: Corresponding funct3 code.
    """
    f3 = {
        # R-Type
        "add": "000", "sub": "000", "addi": "000", "beq": "000", "jalr": "000",
        # I-Type
        "sll": "001", "bne": "001",
        # S-Type
        "slt": "010", "lw": "010", "sw": "010",
        # B-Type
        "sltu": "011", "sltiu": "011",
        # U-Type
        "xor": "100", "blt": "100",
        # J-Type
        "srl": "101", "bge": "101",
        # R-Type Bonus
        "or": "110", "bltu": "110",
        # R-Type Bonus
        "and": "111", "bgeu": "111",
        # U-Type
        "lui": "", "auipc": "", "jal": ""
    }
    return f3.get(x, 'error')

def funct7(x):
    """
    Returns the funct7 code for a given instruction.
    Args:
        x (str): Instruction name.
    Returns:
        str: Corresponding funct7 code.
    """
    
    f7 = {
        "add": "0000000", "sll": "0000000", "slt": "0000000", "sltu": "0000000", "xor": "0000000", "srl": "0000000", "or": "0000000", "and": "0000000",

        "sub": "0100000",

        "lw": "", "addi": "", "sltiu": "", "jalr": "", "sw": "", "beq": "", "bne": "", "blt": "", "bge": "", "bltu": "", "bgeu": "", "lui": "", "auipc": "", "jal": ""
    }
    return f7.get(x, 'error')

def register_code(x):
    """
    Returns the binary code for a given register.
    Args:
        x (str): Register name (e.g., "zero", "s0").
    Returns:
        str: Corresponding 5-bit binary code.
    """
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
    """
    Computes the 2's complement of a binary string.
    Args:
        binary_str (str): Binary string.
        length (int): Desired length of the output binary string.
    Returns:
        str: 2's complement of the input binary string.
    """
    flipped = ''.join('1' if bit == '0' else '0' for bit in binary_str)
    binary = bin(int(flipped, 2) + 1)[2:] 
    return binary.zfill(length)
#print(compute_2s_complement((conversion_to_bits(256,12)),10))

def conversion_to_bits(num, length):
    """
    Converts a number to a binary string of the specified length.
    Args:
        num (int): Number to convert.
        length (int): Desired length of the binary string.
    Returns:
        str: Binary representation of the number.
    """
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

def imm(x, opco):
    """
    Computes the immediate value for an instruction.
    Args:
        x (str): Immediate value as a string.
        opco (str): Opcode of the instruction.
    Returns:
        str: Binary representation of the immediate value.
    """
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
    """
    Processes labels in the assembly code and replaces them with their corresponding addresses.
    Args:
        assembly (list): List of assembly instructions.
    Returns:
        list: Processed assembly instructions with labels replaced by addresses.
    """
    for i in range(0,len(assembly)):
        assembly[i]=assembly[i].lstrip()
    dictlabels=dict()
    for i in range(0,len(assembly)):
        if ':' in assembly[i]:
            labelname=''
            for j in assembly[i]:
                if(j!=':'):
                    labelname+=j
                else:
                    break
            dictlabels[labelname]=i*4
            assembly[i]=assembly[i][assembly[i].index(':')+1:]
    for i in range(0,len(assembly)):
        assembly[i]=assembly[i].lstrip()

    for i in assembly:
        for j in dictlabels.keys():
            if j in i:
                ind=assembly.index(i)
                i=i.replace(j,str(dictlabels[j]-(ind*4)))
                assembly.pop(ind)
                assembly.insert(ind,i)
            else:
                continue
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
            reg1_code = register_code(inst[1])  # Error Resolved of the Register interplaced and rearranging the fucnt3 values
            reg2_code = register_code(t[1].strip(')'))
            funct3_value = funct3(inst[0])
            bineq = imm_value + reg2_code +funct3_value + reg1_code + opco

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