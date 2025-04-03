import sys

file_input = sys.argv[1]
file_output = sys.argv[2]

def band(a, b):
    return a & b

def bin_to_hexhelper(a):
    num = sum(pow(2, i) * int(b) for i, b in enumerate(a[::-1]))
    return str(num)

def bintohex(a):
    dict = {"1111": 'f', "1110": "e", "1101": "d", "1100": "c", "1011": "b", "1010": "a"}
    return "".join(dict.get(a[i * 4:(i + 1) * 4], bin_to_hexhelper(a[i * 4:(i + 1) * 4])) for i in range(8))

def signed32bit(a):
    return "1" + "0" * (32 - len(a)) + a[1:] if a[0] == "1" else "0" + "0" * (32 - len(a)) + a[1:]

def main2comp(var):
    a_passed = signed32bit(dtbsigned(var))
    if a_passed[0] == "0":
        return a_passed
    a = a_passed[1:]
    if int(a[1:]) == 0:
        return "1" + a[1:]
    b = ["1" if x == "0" else "0" for x in a]
    j = len(a) - 1
    while b[j] == "1":
        b[j] = "0"
        j -= 1
    b[j] = "1"
    return "1" + "".join(b)

def unsigned_binary_to_dec(a):
    return sum(2 ** i for i in range(len(a) - 1, -1, -1) if a[i] == "1")

def make32bit(a):
    return (32 - len(a)) * a[0] + a

def dtbsigned(a_passed):
    if a_passed == 0:
        return "0" * 32
    a = abs(a_passed)
    signedbit = "1" if a_passed < 0 else "0"
    st = bin(a)[2:]
    return signedbit + st

def bintd(a):
    if str(a)[0] == "1":
        a_new = twocomp(a)
        b = a_new[::-1]
    else:
        b = (str(a)[::-1])
    ans = sum(pow(2, i) * int(b[i]) for i in range(len(b) - 1))
    return -ans if b[-1] == "1" else ans

def twocomp(a_passed):
    if len(a_passed) == 0 or a_passed == "0" * len(a_passed):
        return "0" * 32
    a = a_passed[1:]
    if int(a) == 0:
        return "1" + a
    b = ["1" if x == "0" else "0" for x in a]
    j = len(a) - 1
    while b[j] == "1":
        b[j] = "0"
        j -= 1
    b[j] = "1"
    return "1" + "".join(b)

# def xor(a, b):
#     return a ^ b

def bor(a, b):
    return a | b

def rightshiftlogical(a, b):
    if b == 0:
        return a
    elif b >= 32:
        return 0
    else:
        return a >> b

def overwritebin():
    with open(file_output, 'w') as bincode:
        pass

def readinst(pc):
    if (pc // 4) >= len(assembly):
        raise IndexError("Program counter out of bounds")
    return assembly[pc // 4]

def ito2(n, b):
    mask = (1 << b) - 1
    return "{:0{}b}".format(n & mask, b)

def dec(imm):
    return int(imm, 2)

def writestatus(reg, pc):
    with open(file_output, "a") as a:
        a.write(f"0b{ito2(pc, 32)} ")
        x=[pc]+ [reg[f"{i:05b}"][1] for i in range(32)]
        print(x)
        for i in range(32):
            if i == 31: 
                a.write(f"0b{ito2(registers[f'{i:05b}'][1], 32)}\n")
            else:
                a.write(f"0b{ito2(registers[f'{i:05b}'][1], 32)} ")
        

def writememory(mem):
    with open(file_output, "a") as a:
        for i in range(32):
            addr = 0x00010000 + (i * 4)
            val = mem.get(hex(addr)[2:], 0)
            print(f"0x{addr:08X}:{val}")
            # print(f"0x{addr:08X}:0b{ito2(val, 32)}")
            a.write(f"0x{addr:08X}:0b{ito2(val, 32)} \n")

fname = file_input
with open(fname, 'r') as a:
    assembly = [line.strip() for line in a if line.strip()]

overwritebin()

registers = {
    '00000': ['zero', 0], '00001': ["ra", 0], '00010': ["sp", 380], '00011': ["gp", 0], '00100': ["tp", 0],
    '00101': ["t0", 0], '00110': ["t1", 0], '00111': ["t2", 0], '01000': ["s0", 0], '01001': ["s1", 0],
    '01010': ["a0", 0], '01011': ["a1", 0], '01100': ["a2", 0], '01101': ["a3", 0], '01110': ["a4", 0],
    '01111': ["a5", 0], '10000': ["a6", 0], '10001': ["a7", 0], '10010': ["s2", 0], '10011': ["s3", 0],
    '10100': ["s4", 0], '10101': ["s5", 0], '10110': ["s6", 0], '10111': ["s7", 0], '11000': ["s8", 0],
    '11001': ["s9", 0], '11010': ["s10", 0], '11011': ["s11", 0], '11100': ["t3", 0], '11101': ["t4", 0],
    '11110': ["t5", 0], '11111': ["t6", 0]
}

memory = {f'{hex(0x10000 + i * 4)[2:]}': 0 for i in range(32)}
# print(memory)
# sys.exit(0)


l = []
def check(l):
    global registers
    global memory

    if l[0] == '00000000100000000000101000010011':
        pass


pc = 0


def r(bineq):
    global registers
    global memory

    instruction = {
        "opcode": bineq[25:32],
        "funct3": bineq[17:20],
        "funct7": bineq[0:7],
        "rd": bineq[20:25],
        "rs1": bineq[12:17],
        "rs2": bineq[7:12],
    }

    op = instruction["opcode"]
    f3 = instruction["funct3"]
    f7 = instruction["funct7"]
    d = instruction["rd"]
    rsrc1 = instruction["rs1"]
    rsrc2 = instruction["rs2"]

    if f3 == '000' and f7 == '0000000':
        registers[d][1] = registers[rsrc1][1] + registers[rsrc2][1]
    elif f3 == '000' and f7 == '0100000':
        registers[d][1] = registers[rsrc1][1] - registers[rsrc2][1]
    elif f3 == '010':
        registers[d][1] = 1 if registers[rsrc1][1] < registers[rsrc2][1] else 0
    elif f3 == '101':
        b = registers[rsrc2][1]
        lower_5_bits_in_dec = unsigned_binary_to_dec(make32bit(twocomp(dtbsigned(b)))[-5:])
        registers[d][1] = rightshiftlogical(registers[rsrc1][1], lower_5_bits_in_dec)
    elif f3 == '110':
        registers[d][1] = bor(registers[rsrc1][1], registers[rsrc2][1])
    elif f3 == '111':
        registers[d][1] = band(registers[rsrc1][1], registers[rsrc2][1])
    return 4

def i(bineq):
    global registers
    global memory

    instruction = {
        "opcode": bineq[25:32],
        "funct3": bineq[17:20],
        "rd": bineq[20:25],
        "rs1": bineq[12:17],
        "imm": bineq[0:12],
    }

    op = instruction["opcode"]
    d = instruction["rd"]
    rsrc1 = instruction["rs1"]
    i_type_imm = instruction["imm"]

    imm_i_32_bit = make32bit(i_type_imm)
    number = bintd(imm_i_32_bit)

    if op == "0000011":  # Load
        address = registers[rsrc1][1] + number

        if address % 4 != 0:
            address -= address % 4

        location_key = hex(0x10000 + address)[2:]
        if location_key not in memory:
            memory[location_key] = 0
        registers[d][1] = memory[location_key]

    elif op == "0010011": 
        registers[d][1] = registers[rsrc1][1] + number

    elif op == "1100111":
        imm_i_32_bit = make32bit(i_type_imm)
        number = bintd(imm_i_32_bit)
        address = (registers[rsrc1][1] + number) & 0xFFFFFFFE
        registers[d][1] = pc + 4
        registers['00000'][1] = 0
        return str(address)

    return 4

def s(bineq):
    global registers
    global memory

    instruction = {
        "opcode": bineq[25:32],
        "funct3": bineq[17:20],
        "rs1": bineq[12:17],
        "rs2": bineq[7:12],
        "imm": bineq[0:7] + bineq[20:25],
    }

    imm = instruction["imm"]
    rs1 = instruction["rs1"]
    rs2 = instruction["rs2"]

    if imm[0] == "0":
        imm_val = int(imm, 2)
    else:
        imm_val = int(imm, 2) - (1 << 12)

    if dtbsigned(registers[rs1][1])[0] == "0":
        value1 = registers[rs1][1]
    else:
        value1 = registers[rs1][1] - (1 << 32)

    address = value1 + imm_val

    if dtbsigned(registers[rs2][1])[0] == "0":
        value2 = registers[rs2][1]
    else:
        value2 = registers[rs2][1] - (1 << 32)

    memory[hex(address)[2:]] = value2 & 0xFFFFFFFF

    return 4

def bt(bineq):
    global registers
    global memory

    instruction = {
        "opcode": bineq[25:32],
        "funct3": bineq[17:20],
        "rs1": bineq[12:17],
        "rs2": bineq[7:12],
        "imm": bineq[0] + bineq[24] + bineq[1:7] + bineq[20:24] + "0",
    }

    f3 = instruction["funct3"]
    rsrc1 = instruction["rs1"]
    rsrc2 = instruction["rs2"]
    imm = instruction["imm"]

    condition = False
    if f3 == "000":
        condition = registers[rsrc1][1] == registers[rsrc2][1]
    elif f3 == "001":
        condition = registers[rsrc1][1] != registers[rsrc2][1]

    if condition:
        imm_32 = make32bit(imm)
        return bintd(imm_32)
    return 4

def j(bineq):
    global registers
    global memory

    instruction = {
        "opcode": bineq[25:32],
        "rd": bineq[20:25],
        "imm": bineq[0] + bineq[12:20] + bineq[11] + bineq[1:11] + "0",
    }

    op = instruction["opcode"]
    d = instruction["rd"]
    imm = instruction["imm"]

    if op == "1101111":
        registers[d][1] = pc + 4
        imm_i_32_bit = make32bit(imm)
        return bintd(imm_i_32_bit)
    
    registers['00000'][1] = 0
    return 4

def bonus(bineq):
    global registers
    global memory

    instruction = {
        "opcode": bineq[25:32],
        "funct3": bineq[17:20],
        "funct7": bineq[0:7],
        "rd": bineq[20:25],
        "rs1": bineq[12:17],
        "rs2": bineq[7:12],
    }

    op = instruction["opcode"]
    f3 = instruction["funct3"]
    f7 = instruction["funct7"]
    d = instruction["rd"]
    rsrc1 = instruction["rs1"]
    rsrc2 = instruction["rs2"]

    if f3 == '000':
        registers[d][1] = registers[rsrc1][1] * registers[rsrc2][1]

    elif f3 == '001':
        registers[rsrc1][1] = 0

    elif f3 == '010':
        value = registers[rsrc1][1]
        gg = int(bin(value)[2:].zfill(32)[::-1], 2)
        registers[d][1] = gg

    elif f3 == '011':
        writestatus(registers, pc)
        writememory(memory)
        sys.exit(0)
    return 4

def segregate_instruction(bineq):
    global registers

    # print(bineq)
    # l.append(bineq)

    registers['00000'][1] = 0
    opcode = bineq[25:32]
    if opcode == "0110011":  
        return r(bineq)
    elif opcode in ["0000011", "0010011", "1100111"]:  
        return i(bineq)
    elif opcode == "0100011":  
        return s(bineq)
    elif opcode == "1100011":  
        return bt(bineq)
    elif opcode == "1101111":  
        return j(bineq)
    
    if bineq[0:7] == "0000001":
        return bonus(bineq)
    return None

while (pc // 4) < len(assembly):
    try:
        bineq = readinst(pc)
    except IndexError:
        break

    instruction_result = segregate_instruction(bineq)

    if bineq == "00000000000000000000000001100011":
        writestatus(registers, pc)
        break
    
    if isinstance(instruction_result, str): 
        pc = int(instruction_result)
    else:
        pc += instruction_result
    writestatus(registers, pc)

writememory(memory)


# print('''0b00000000000000000000000000000100 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000100000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000'''=='''0b00000000000000000000000000000100 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000100000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000000000000000000''')