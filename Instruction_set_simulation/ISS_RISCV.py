registerFiles = {f"x{i}": 0 for i in range(32)}
dataMemory = {0x10010000 + i * 4: 0 for i in range(128)}  # Predefined memory block
pc = 0

# Define execution logic for R-type instructions
def executeR(funct3, funct7, rd, rs1, rs2):
    rs1_val = registerFiles[rs1]
    rs2_val = registerFiles[rs2]
    if funct3 == "000":
        if funct7 == "0000000":  # ADD
            registerFiles[rd] = rs1_val + rs2_val
        elif funct7 == "0100000":  # SUB
            registerFiles[rd] = rs1_val - rs2_val
    elif funct3 == "111":  # AND
        registerFiles[rd] = rs1_val & rs2_val
    elif funct3 == "110":  # OR
        registerFiles[rd] = rs1_val | rs2_val
    elif funct3 == "100":  # XOR
        registerFiles[rd] = rs1_val ^ rs2_val
    elif funct3 == "001":  # SLL (Shift Left Logical)
        registerFiles[rd] = rs1_val << (rs2_val & 0x1F)
    elif funct3 == "101":
        if funct7 == "0000000":  # SRL (Shift Right Logical)
            registerFiles[rd] = (rs1_val >> (rs2_val & 0x1F)) & 0xFFFFFFFF
        elif funct7 == "0100000":  # SRA (Shift Right Arithmetic)
            registerFiles[rd] = rs1_val >> (rs2_val & 0x1F)

# Define execution logic for I-type instructions
def executeI(funct3, rd, rs1, imm):
    rs1_val = registerFiles[rs1]
    if funct3 == "000":  # ADDI
        registerFiles[rd] = rs1_val + imm
    elif funct3 == "100":  # XORI
        registerFiles[rd] = rs1_val ^ imm
    elif funct3 == "110":  # ORI
        registerFiles[rd] = rs1_val | imm
    elif funct3 == "111":  # ANDI
        registerFiles[rd] = rs1_val & imm
    elif funct3 == "001":  # SLLI
        registerFiles[rd] = rs1_val << (imm & 0x1F)
    elif funct3 == "101":
        if imm >> 10 == 0:  # SRLI
            registerFiles[rd] = (rs1_val >> (imm & 0x1F)) & 0xFFFFFFFF
        else:  # SRAI
            registerFiles[rd] = rs1_val >> (imm & 0x1F)

# Define execution logic for B-type instructions
def executeB(funct3, rs1, rs2, imm):
    global pc
    rs1_val = registerFiles[rs1]
    rs2_val = registerFiles[rs2]
    if funct3 == "000":  # BEQ
        if rs1_val == rs2_val:
            pc += imm // 4
    elif funct3 == "001":  # BNE
        if rs1_val != rs2_val:
            pc += imm // 4
    elif funct3 == "100":  # BLT
        if rs1_val < rs2_val:
            pc += imm // 4
    elif funct3 == "101":  # BGE
        if rs1_val >= rs2_val:
            pc += imm // 4

# Define execution logic for U-type instructions
def executeU(opcode, rd, imm):
    global pc
    if opcode == "0110111":  # LUI
        registerFiles[rd] = imm << 12
    elif opcode == "0010111":  # AUIPC
        registerFiles[rd] = pc + (imm << 12)

# Define execution logic for J-type instructions
def executeJ(rd, imm):
    global pc
    registerFiles[rd] = pc + 4
    pc += imm // 4

# Decode and execute instructions
def instDecoder(inst):
    opcode = inst[25:32]
    if opcode == "0110011":  # R-type instruction
        funct3 = inst[17:20]
        funct7 = inst[0:7]
        rd = f"x{int(inst[20:25], 2)}"
        rs1 = f"x{int(inst[12:17], 2)}"
        rs2 = f"x{int(inst[7:12], 2)}"
        executeR(funct3, funct7, rd, rs1, rs2)
    elif opcode == "0010011":  # I-type instruction
        funct3 = inst[17:20]
        rd = f"x{int(inst[20:25], 2)}"
        rs1 = f"x{int(inst[12:17], 2)}"
        imm = int(inst[0:12], 2) if inst[0] == "0" else -((1 << 12) - int(inst[0:12], 2))
        executeI(funct3, rd, rs1, imm)
    elif opcode == "1100011":  # B-type instruction
        funct3 = inst[17:20]
        rs1 = f"x{int(inst[12:17], 2)}"
        rs2 = f"x{int(inst[7:12], 2)}"
        imm = int(inst[0] + inst[24] + inst[1:7] + inst[20:24], 2) << 1
        if inst[0] == "1":
            imm -= 1 << 13
        executeB(funct3, rs1, rs2, imm)
    elif opcode in ["0110111", "0010111"]:  # U-type instruction
        rd = f"x{int(inst[20:25], 2)}"
        imm = int(inst[0:20], 2)
        executeU(opcode, rd, imm)
    elif opcode == "1101111":  # J-type instruction
        rd = f"x{int(inst[20:25], 2)}"
        imm = int(inst[0] + inst[12:20] + inst[11] + inst[1:11], 2) << 1
        if inst[0] == "1":
            imm -= 1 << 21
        executeJ(rd, imm)

# Load binary instructions from file
def loadInstructions(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]

# Write memory to output file
def writeMemory(filename):
    with open(filename, "w") as file:
        addresses = sorted(dataMemory.keys())
        for i in range(0, len(addresses), 8):
            line = f"{hex(addresses[i])}"
            for j in range(8):
                addr = addresses[i + j]
                line += f"    {hex(dataMemory[addr] & 0xFFFFFFFF)}"
            file.write(line + "\n")

# Main simulator loop
def simulate(inputFile, outputFile):
    global pc
    instructions = loadInstructions(inputFile)
    while pc < len(instructions):
        inst = instructions[pc]
        instDecoder(inst)
        pc += 1
    writeMemory(outputFile)

# Example usage
simulate("C:\\Users\\MSI\\Desktop\\RISC_v\\Instruction_set_simulation\\input.bin", "C:\\Users\\MSI\\Desktop\\RISC_v\\Instruction_set_simulation\\output.txt")
