# Dictionaries for opcode, funct3, funct7, and registers
opcode = {
    "R_TYPE" : "0110011",
    "I_TYPE" : "0010011",
    "I_LOAD" : "0000011",
    "S_TYPE" : "0100011",
    "B_TYPE" : "1100011",
    "J_TYPE" : "1101111",
    "JALR" : "1100111",
    "U_TYPE" : "0110111",
    "AUIPC" : "0010111"
}

R_TYPE = {"add", "sub", "xor", "or", "and", "sll", "srl", "slt", "sltu", "sra"}
I_TYPE = {"addi", "xori", "ori", "andi", "slli", "srli", "slti", "sltiu", "lw", "jalr", "srai"}
S_TYPE = {"sw"}
B_TYPE = {"beq", "bne", "blt", "bge", "bltu", "bgeu"}
U_TYPE = {"lui", "li", "auipc"}
J_TYPE = {"jal"}

funct3 = {
    "add": "000", "sub": "000", 
    "xor" : "100", "or" : "110",
    "and" : "111",
    "sll" : "001", "srl" : "101",
    "slt" : "010", "sltu" : "011",
    "addi": "000", 
    "xori" : "100", "ori" : "110",
    "andi" : "111",
    "slli" : "001", "srli" : "101",
    "slti" : "010", "sltiu" : "011",
    "lw": "010", "sw": "010", 
    "beq": "000", "bne" : "001",
    "blt" : "100", "bge" : "101",
    "jalr" : "000",
    "srai": "101",  
    "sra": "101",   
    "bltu": "110",  
    "bgeu": "111"
}

funct7 = {
    "add": "0000000", "sub": "0100000", 
    "xor" : "0000000", "or" : "0000000",
    "and" : "0000000",
    "sll" : "0000000", "srl" : "0000000",
    "slt" : "0000000", "sltu" : "0000000",
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
print(lines)
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
line = []
keys = []
for i, word in enumerate(sample):
    if word.find("j ") == 0:
        keys = word.split()
        word = f"jal x0, {keys[1]}\n"  # Mặc định x0 cho lệnh `j`

    elif word.find("jal ") == 0:
        keys = word.split()
        if "," not in keys[1]:  # Nếu thiếu `rd`, mặc định x1 là rd
            word = f"jal x1, {keys[1]}\n"

    elif word.find("jalr ") == 0:
        keys = word.split()
        # Đảm bảo trường hợp thiếu các tham số thì bổ sung mặc định
        if len(keys) == 2:  # Chỉ có rd và rs1
            word = f"jalr {keys[1]}, x1, 0\n"  # Mặc định offset = 0
        elif len(keys) == 3:  # Có rd, rs1 nhưng thiếu offset
            if "(" in keys[2]:  # Kiểm tra xem rs1 có trong dạng offset(rs1)
                pos = keys[2].find("(")
                offset = keys[2][:pos] if pos != -1 else "0"
                rs1 = keys[2][pos + 1:keys[2].find(")")]
                word = f"jalr {keys[1]} {rs1}, {offset}\n"
            else:
                word = f"jalr {keys[1]} {keys[2]} 0\n"  # Mặc định offset = 0 nếu không có
        elif len(keys) == 4:  # Đã đủ cả rd, rs1, offset
            word = f"jalr {keys[1]}, {keys[2]}, {keys[3]}\n"

    elif word.find("nop") == 0:
        word = "addi x0, x0, 0\n"
    elif word.find("li ") == 0:
        keys = word.split()
        keys[0] = "addi "
        keys[2] = " x0, " + keys[2]
        word = keys[0] + keys[1] + keys[2] + "\n"
    elif word.find("bgt ") == 0:
        keys = word.split()
        word = "blt" + " " + keys[2][:-1] + ", " + keys[1] + " " + keys[3] + "\n"
    line.append(word.lstrip())

with open("C:\\Users\\MSI\\Desktop\\RISC_v\\RISC_V_assembler\\raw_input.txt", "w") as ripf:   
    ripf.writelines(line)

def to_twos_complement(n, bits):
    if n < 0:
        n = (1 << bits) + n  # Chuyển số âm sang bù 2
    return bin(n)

# format label to bin 
def label_bin(label, pc):
    print(label_dict[label], "-", pc)
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
        if word[0] == "lw":                 #I-LOAD
            pos = word[2].find("(")
            temp = word[2][:pos]
            rs1 = word[2][pos+1:(word[2].find(")"))]
            print(imm(temp)[-12:])
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
        print(i)
        output = i[19] + i[21:27] + registers[word[2]] + registers[word[1]] + funct3[word[0]] + i[27:31] + i[20] + opcode["B_TYPE"]
    elif word[0] in U_TYPE:                 #U-TYPE                             
        i = imm(word[2])
        if (word[0] == "auipc"):            #AUIPC
            output = i[-20:] + registers[word[1]] + opcode["AUIPC"]
        else:
            output = i[-20:] + registers[word[1]] + opcode["U_TYPE"]
    elif word[0] in J_TYPE:                 #J-TYPE
        i = label_bin(word[2], pc)
        print(i)
        output = i[11] + i[21:31] + i[20] + i[12:20] + registers[word[1]] + opcode["J_TYPE"]
    else:
        output = bin(0)[2:].zfill(32)
    output_lines.append(output + "\n")
    pc += 4
with open("C:\\Users\\MSI\\Desktop\\RISC_v\\RISC_V_assembler\\output.txt", "w") as opf:   
    opf.writelines(output_lines)           # write to output
    
    
   
    
