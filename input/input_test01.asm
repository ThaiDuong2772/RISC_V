
# R-Type Instructions
add x1, x2, x3      # x1 = x2 + x3
sub x4, x5, x6      # x4 = x5 - x6
xor x7, x8, x9      # x7 = x8 XOR x9
or x10, x11, x12    # x10 = x11 OR x12
and x13, x14, x15   # x13 = x14 AND x15
sll x16, x17, x18   # x16 = x17 << x18 (shift left logical)
srl x19, x20, x21   # x19 = x20 >> x21 (shift right logical)
slt x22, x23, x24   # x22 = (x23 < x24) ? 1 : 0
sltu x25, x26, x27  # x25 = (x26 < x27 unsigned) ? 1 : 0

# I-Type Instructions
addi x1, x2, 10     # x1 = x2 + 10
andi x3, x4, 255    # x3 = x4 AND 255
ori x5, x6, 15      # x5 = x6 OR 15
xori x7, x8, 128    # x7 = x8 XOR 128
li x10, 0x100
lw x9, 0(x10)       # x9 = Memory[x10 + 0]
jalr x11, 0(x12)    # Jump to address in x12 + 0 and store return address in x11

# S-Type Instructions
sw x1, 4(x2)        # Memory[x2 + 4] = x1

# B-Type Instructions
beq x1, x2, label1  # If x1 == x2, jump to label1
bne x3, x4, label2  # If x3 != x4, jump to label2
blt x5, x6, label3  # If x5 < x6, jump to label3
bge x7, x8, label4  # If x7 >= x8, jump to label4

# U-Type Instructions
lui x1, 0x12345     # Load upper immediate: x1 = 0x12345000
auipc x2, 0x10      # Add upper immediate to PC: x2 = PC + 0x10000

# J-Type Instructions
j label5            # Jump to label5
jal x3, label6      # Jump to label6 and store return address in x3

# Labels for branching
label1:
    addi x1, x1, 1  # x1 = x1 + 1
    j end           # Jump to end

label2:
    addi x2, x2, 2  # x2 = x2 + 2
    j end           # Jump to end

label3:
    addi x3, x3, 3  # x3 = x3 + 3
    j end           # Jump to end

label4:
    addi x4, x4, 4  # x4 = x4 + 4
    j end           # Jump to end

label5:
    nop             # No operation

label6:
    nop             # No operation

end:
    nop             # End of program

