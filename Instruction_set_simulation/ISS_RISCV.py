# Initialize registers and memory
dataMemory = {0x10010000 + i * 4: 0 for i in range(128)}  # Predefined memory block
pc = 0x10010000  # Program counter
reg = {i: 0 for i in range(32)}  # General-purpose registers
reg[2] = 2147479548  # Stack pointer (x2)
reg[3] = 268468224   # Global pointer (x3)

# Define execution logic for R-type instructions
def executeR(funct3, funct7, rd, rs1, rs2):
    rs1_val = reg[rs1]
    rs2_val = reg[rs2]
    if funct3 == "000":
        if funct7 == "0000000":  # ADD
            reg[rd] = rs1_val + rs2_val
        elif funct7 == "0100000":  # SUB
            reg[rd] = rs1_val - rs2_val
    elif funct3 == "111":  # AND
        reg[rd] = rs1_val & rs2_val
    elif funct3 == "110":  # OR
        reg[rd] = rs1_val | rs2_val
    elif funct3 == "100":  # XOR
        reg[rd] = rs1_val ^ rs2_val
    elif funct3 == "001":  # SLL (Shift Left Logical)
        reg[rd] = rs1_val << (rs2_val & 0x1F)
    elif funct3 == "101":
        if funct7 == "0000000":  # SRL (Shift Right Logical)
            reg[rd] = (rs1_val >> (rs2_val & 0x1F)) & 0xFFFFFFFF
        elif funct7 == "0100000":  # SRA (Shift Right Arithmetic)
            reg[rd] = rs1_val >> (rs2_val & 0x1F)

# Define execution logic for I-type instructions
def executeI(funct3, rd, rs1, imm):
    rs1_val = reg[rs1]
    if funct3 == "000":  # ADDI
        reg[rd] = rs1_val + imm
    elif funct3 == "100":  # XORI
        reg[rd] = rs1_val ^ imm
    elif funct3 == "110":  # ORI
        reg[rd] = rs1_val | imm
    elif funct3 == "111":  # ANDI
        reg[rd] = rs1_val & imm
    elif funct3 == "001":  # SLLI
        reg[rd] = rs1_val << (imm & 0x1F)
    elif funct3 == "101":
        if imm >> 10 == 0:  # SRLI
            reg[rd] = (rs1_val >> (imm & 0x1F)) & 0xFFFFFFFF
        else:  # SRAI
            reg[rd] = rs1_val >> (imm & 0x1F)

# Define execution logic for S-type instructions
def executeS(funct3, rs1, rs2, imm):
    rs1_val = reg[rs1]
    rs2_val = reg[rs2]
    address = rs1_val + imm
    if address in dataMemory:
        if funct3 == "000":  # SB (Store Byte)
            dataMemory[address] = rs2_val & 0xFF
        elif funct3 == "001":  # SH (Store Halfword)
            dataMemory[address] = rs2_val & 0xFFFF
        elif funct3 == "010":  # SW (Store Word)
            dataMemory[address] = rs2_val & 0xFFFFFFFF
    else:
        print(f"Memory access error at address {hex(address)}")

# Define execution logic for B-type instructions
def executeB(funct3, rs1, rs2, imm):
    global pc
    rs1_val = reg[rs1]
    rs2_val = reg[rs2]
    if funct3 == "000" and rs1_val == rs2_val:  # BEQ
        pc += imm
    elif funct3 == "001" and rs1_val != rs2_val:  # BNE
        pc += imm
    elif funct3 == "100" and rs1_val < rs2_val:  # BLT
        pc += imm
    elif funct3 == "101" and rs1_val >= rs2_val:  # BGE
        pc += imm

# Define execution logic for U-type instructions
def executeU(opcode, rd, imm):
    global pc
    if opcode == "0110111":  # LUI
        reg[rd] = imm << 12
    elif opcode == "0010111":  # AUIPC
        reg[rd] = pc + (imm << 12)

# Define execution logic for J-type instructions
def executeJ(rd, imm):
    global pc
    reg[rd] = pc + 4
    pc += imm

# Decode and execute instructions
def instDecoder(inst):
    opcode = inst[25:32]
    rd = int(inst[20:25], 2)
    rs1 = int(inst[12:17], 2)
    rs2 = int(inst[7:12], 2)
    funct3 = inst[17:20]
    funct7 = inst[0:7]
    imm = None

    if opcode == "0110011":  # R-type
        executeR(funct3, funct7, rd, rs1, rs2)
    elif opcode == "0010011":  # I-type
        imm = int(inst[0:12], 2) if inst[0] == "0" else -((1 << 12) - int(inst[0:12], 2))
        executeI(funct3, rd, rs1, imm)
    elif opcode == "1100011":  # B-type
        imm = int(inst[0] + inst[24] + inst[1:7] + inst[20:24], 2) << 1
        if inst[0] == "1":
            imm -= 1 << 13
        executeB(funct3, rs1, rs2, imm)
    elif opcode == "0100011":  # S-type
        imm = int(inst[0:7] + inst[20:25], 2) if inst[0] == "0" else -((1 << 12) - int(inst[0:7] + inst[20:25], 2))
        executeS(funct3, rs1, rs2, imm)
    elif opcode in ["0110111", "0010111"]:  # U-type
        imm = int(inst[0:20], 2)
        executeU(opcode, rd, imm)
    elif opcode == "1101111":  # J-type
        imm = int(inst[0] + inst[12:20] + inst[11] + inst[1:11], 2) << 1
        if inst[0] == "1":
            imm -= 1 << 21
        executeJ(rd, imm)

# Load binary instructions from file
def loadInstructions(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

# Write memory to output file with standard hexadecimal format
def writeMemory(filename):
    with open(filename, "w") as file:
        addresses = sorted(dataMemory.keys())
        for i in range(0, len(addresses), 8):
            line = f"{hex(addresses[i])}"  # First address in the line
            for j in range(8):
                addr = addresses[i + j]
                # Format each value to 0x00000000 (8 digits with leading zeros)
                value = dataMemory[addr] & 0xFFFFFFFF  # Ensure 32-bit value
                formatted_value = f"0x{value:08x}"  # Format value as 0x followed by 8 hexadecimal digits
                line += f" {formatted_value}"
            file.write(line + "\n")


# Main simulator loop
def simulate(inputFile, outputFile):
    global pc
    instructions = loadInstructions(inputFile)
    if not instructions:
        print("No instructions to execute.")
        return
    while pc < (len(instructions) * 4 + 0x10010000):
        inst = instructions[int((pc - 0x10010000) / 4)]
        instDecoder(inst)
        pc += 4
    writeMemory(outputFile)

# Example usage
simulate("C:\\Users\\MSI\\Desktop\\RISC_v\\Instruction_set_simulation\\input.bin", "C:\\Users\\MSI\\Desktop\\RISC_v\\Instruction_set_simulation\\output.txt")