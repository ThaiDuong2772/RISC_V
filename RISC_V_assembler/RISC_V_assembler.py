# Dictionaries for opcode, funct3, funct7, and registers
opcode = {
    "R_TYPE": "0110011",
    "I_TYPE": "0010011",
    "I_LOAD": "0000011",
    "S_TYPE": "0100011",
    "B_TYPE": "1100011",
    "J_TYPE": "1101111",
    "JALR": "1100111",
    "U_TYPE": "0110111",
    "AUIPC": "0010111"
}

R_TYPE = {"add", "sub", "xor", "or", "and", "sll", "srl", "slt", "sltu", "sra"}
I_TYPE = {"addi", "xori", "ori", "andi", "slli", "srli", "slti", "sltiu", "lw", "jalr", "srai", "lh", "lb", "lhu", "lbu"}
S_TYPE = {"sw", "sh", "sb"}
B_TYPE = {"beq", "bne", "blt", "bge", "bltu", "bgeu"}
U_TYPE = {"lui", "li", "auipc"}
J_TYPE = {"jal"}

funct3 = {
    "add": "000", "sub": "000",
    "xor": "100", "or": "110",
    "and": "111",
    "sll": "001", "srl": "101",
    "slt": "010", "sltu": "011",
    "addi": "000",
    "xori": "100", "ori": "110",
    "andi": "111",
    "slli": "001", "srli": "101",
    "slti": "010", "sltiu": "011",
    "lw": "010", "lh": "001", "lb": "000", "lhu": "101", "lbu": "100",
    "sw": "010", "sh": "001", "sb": "000",
    "beq": "000", "bne": "001",
    "blt": "100", "bge": "101",
    "jalr": "000",
    "srai": "101",
    "sra": "101",
    "bltu": "110",
    "bgeu": "111"
}

funct7 = {
    "add": "0000000", "sub": "0100000",
    "xor": "0000000", "or": "0000000",
    "and": "0000000",
    "sll": "0000000", "srl": "0000000",
    "slt": "0000000", "sltu": "0000000",
    "sra": "0100000",
    "srai": "0100000"
}

registers = {
    "x0": "00000", "x1": "00001", "x2": "00010",
    "x3": "00011", "x4": "00100", "x5": "00101",
    "x6": "00110", "x7": "00111", "x8": "01000",
    "x9": "01001", "x10": "01010", "x11": "01011",
    "x12": "01100", "x13": "01101", "x14": "01110",
    "x15": "01111", "x16": "10000", "x17": "10001",
    "x18": "10010", "x19": "10011", "x20": "10100",
    "x21": "10101", "x22": "10110", "x23": "10111",
    "x24": "11000", "x25": "11001", "x26": "11010",
    "x27": "11011", "x28": "11100", "x29": "11101",
    "x30": "11110", "x31": "11111"
}

def imm(x):
    if x.find("0x") != -1:
        i = bin(int(x[2:], 16))[2:].zfill(32)
        return i
    elif int(x) < 0:
        return to_twos_complement(int(x), 32)
    return bin(int(x))[2:].zfill(32)

with open("C:\\Users\\MSI\\Desktop\\RISC_v\\RISC_V_assembler\\input.txt", "r") as ipf:
    input_lines = ipf.readlines()  # Rename the variable to avoid conflict

# Dictionaries for Label
labels = []
pos_label = []
lines = []

# Remove comments from lines
for line in input_lines:
    cmt = line.find("#")
    if cmt != -1:
        if cmt != 0:
            fixed_line = line[:cmt] + "\n"
            if len(line) > 1:
                lines.append(fixed_line.lstrip())
    else:
        if len(line) > 1:
            lines.append(line.lstrip())

# Process labels and update lines
count = 4
for i in range(0, len(lines)):
    pos = lines[i].find(":")
    if pos != -1:
        labels.append(lines[i][:pos])
        count -= 4
        pos_label.append(count)
        lines[i] = lines[i][pos+1:].lstrip()
    count += 4

label_dict = {labels[i]: pos_label[i] for i in range(len(labels))}

# Write the cleaned lines to a new file
with open("C:\\Users\\MSI\\Desktop\\RISC_v\\RISC_V_assembler\\raw_input.txt", "w") as ripf:
    ripf.writelines(lines)


# format file

with open("C:\\Users\\MSI\\Desktop\\RISC_v\\RISC_V_assembler\\raw_input.txt", "r") as ripf:
    sample = ripf.readlines()
formatted_lines = []
flag = 0
for line in sample:
    keys = line.split()
    for key in keys:
        if key in label_dict:
            label_dict[key] += 4*flag
    if line.startswith("j "):
        _, target = line.split()
        formatted_lines.append(f"jal x0, {target}\n")
    elif line.startswith("jal "):
        parts = line.split()
        if len(parts) == 2:
            formatted_lines.append(f"jal x1, {parts[1]}\n")
        else:
            formatted_lines.append(line)
    elif line.startswith("jalr "):
        parts = line.split()
        if len(parts) == 2:
            formatted_lines.append(f"jalr {parts[1]} x1, 0\n")
        elif len(parts) == 3:
            offset, rs1 = parts[2].split("(")
            rs1 = rs1.rstrip(")")
            formatted_lines.append(f"jalr {parts[1]} {rs1} {offset}\n")
        else:
            formatted_lines.append(line)
    elif line.startswith("nop"):
        formatted_lines.append("addi x0, x0, 0\n")
    elif line.startswith("li "):
        _, rd, imm_val = line.split()
        imm_val = int(imm_val, 16) if "0x" in imm_val else int(imm_val)
        if imm_val >= 0x1000:
            upper = imm_val >> 12
            lower = imm_val & 0xFFF
            formatted_lines.append(f"lui {rd} {upper}\n")
            flag += 1
            formatted_lines.append(f"addi {rd} {rd} {lower}\n")
        else:
            formatted_lines.append(f"addi {rd} x0, {imm_val}\n")
    elif line.startswith("bgt "):
        _, rs1, rs2, label = line.split()
        formatted_lines.append(f"blt {rs2} {rs1} {label}\n")
    else:
        formatted_lines.append(line)

with open("C:\\Users\\MSI\\Desktop\\RISC_v\\RISC_V_assembler\\raw_input.txt", "w") as ripf:
    ripf.writelines(formatted_lines)

def to_twos_complement(n, bits):
    if n < 0:
        n = (1 << bits) + n  # Chuyển số âm sang bù 2
    return bin(n)

# format label to bin 
def label_bin(label, pc):
    imm = label_dict[label] - pc
    if imm < 0:
        imm = to_twos_complement(imm, 32)[2:]
    else:
        imm = bin(imm)[2:]
        imm = imm.zfill(32)
    return imm

with open("C:\\Users\\MSI\\Desktop\\RISC_v\\RISC_V_assembler\\raw_input.txt", "r") as ripf:
    input = ripf.readlines()

# assembler
pc = 0
output_lines = []
#immediate = []
for line in input:
    word = line.split()
    for i in range(1, len(word)):
        if word[i].find(",") != -1:
            word[i] = word[i][:word[i].find(",")]
        #try:
        #    int(word[i])
        #    immediate.append(word[i])
        #except ValueError:
        #    continue    

    if word[0] in R_TYPE:                   #R-TYPE
        output = funct7[word[0]] + registers[word[3]] + registers[word[2]] + funct3[word[0]] + registers[word[1]] + opcode["R_TYPE"]
    elif word[0] in I_TYPE:                 #I-TYPE
        if word[0] in {"lw", "lh", "lb", "lhu", "lbu"}:                 #I-LOAD
            pos = word[2].find("(")
            temp = word[2][:pos]
            rs1 = word[2][pos+1:(word[2].find(")"))]
            output = imm(temp)[-12:] + registers[rs1] + funct3[word[0]] + registers[word[1]] + opcode["I_LOAD"]
        elif word[0] == "jalr":
            output = imm(word[3])[-12:] + registers[word[2]] + funct3[word[0]] + registers[word[1]] + opcode["JALR"]
        elif word[0] == "srai":
            output = funct7[word[0]] + imm(word[3])[-5:] + registers[word[2]] + funct3[word[0]] + registers[word[1]] + opcode["I_TYPE"]
        else:
            output = imm(word[3])[-12:] + registers[word[2]] + funct3[word[0]] + registers[word[1]] + opcode["I_TYPE"]
    elif word[0] in S_TYPE:                 #S-TYPE
        pos = word[2].find("(")
        temp = word[2][:pos]
        rs1 = word[2][pos+1:(word[2].find(")"))]
        output = imm(temp)[-12:-5] + registers[word[1]] + registers[rs1] + funct3[word[0]] + imm(temp)[-5:] + opcode["S_TYPE"]
    elif word[0] in B_TYPE:                 #B-TYPE
        i = label_bin(word[3], pc)
        output = i[19] + i[21:27] + registers[word[2]] + registers[word[1]] + funct3[word[0]] + i[27:31] + i[20] + opcode["B_TYPE"]
    elif word[0] in U_TYPE:                 #U-TYPE                             
        i = imm(word[2])
        if (word[0] == "auipc"):            #AUIPC
            output = i[-20:] + registers[word[1]] + opcode["AUIPC"]
        else:
            output = i[-20:] + registers[word[1]] + opcode["U_TYPE"]
    elif word[0] in J_TYPE:                 #J-TYPE
        i = label_bin(word[2], pc)
        print(registers[word[1]])
        output = i[11] + i[21:31] + i[20] + i[12:20] + registers[word[1]] + opcode["J_TYPE"]
    else:
        output = bin(0)[2:].zfill(32)
    output_lines.append(output + "\n")
    pc += 4
with open("C:\\Users\\MSI\\Desktop\\RISC_v\\RISC_V_assembler\\output.txt", "w") as opf:   
    opf.writelines(output_lines)           # write to output
    
    
   
    
