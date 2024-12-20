li x17, 1          # a7
li x10, 15         # a0
li x11, -5         # a1
li x12, 5          # a2
add x13, x10, x11  # a3 = a0 + a1
sub x14, x10, x12  # a4 = a0 - a2 # expected: x13=x14=10
addi x15, x15, 0   # a5 (no stall test)
beq x14, x13, valid0
jal x1, error

valid0:
auipc x13, 1       # a3
lui x14, 1         # a4
addi x14, x14, 36  # a4 = 4128
beq x14, x13, valid1
jal x1, error

valid1:
li x10, 0xc        # a0
li x11, 0xa        # a1
and x12, x11, x10  # a2 = a1 & a0
or x13, x11, x10   # a3 = a1 | a0
li x14, 0x6        # a4
xor x15, x13, x14  # a5 = a3 ^ a4 # expected: x12=x15=8
beq x12, x15, valid2
jal x1, error

valid2:
andi x12, x10, 0xa # a2 = a0 & 0xa
ori x13, x10, 0xa  # a3 = a0 | 0xa
xori x15, x13, 0x6 # a5 = a3 ^ 0x6 # expected: x12=x15=8
beq x12, x15, valid3
jal x1, error

valid3:
li x10, 1          # a0
li x11, -1         # a1
slt x12, x10, x11  # a2 = (a0 < a1)
sltu x13, x10, x11 # a3 = (unsigned a0 < a1)
addi x12, x12, 1   # a2 = a2 + 1
beq x12, x13, valid4
jal x1, error

valid4:
slti x12, x10, -1  # a2 = (a0 < -1)
sltiu x13, x10, -1 # a3 = (unsigned a0 < -1)
addi x12, x12, 1   # a2 = a2 + 1
beq x12, x13, valid5
jal x1, error

valid5:
li x11, 2          # a1
sll x12, x10, x11  # a2 = a0 << a1
srl x12, x12, x10  # a2 = a2 >> a0
slli x13, x10, 2   # a3 = a0 << 2
srli x13, x13, 1   # a3 = a3 >> 1 # expected: x12=x13=2
beq x12, x13, valid6
jal x1, error

valid6:
li x10, -8         # a0
li x14, 2          # a4
srai x12, x10, 2   # a2 = a0 >> 2 (arithmetic)
sra x13, x10, x14  # a3 = a0 >> a4 (arithmetic) # expected: x12=x13=-2
beq x12, x13, valid7
jal x1, error

valid7:
jal x1, procedure
beq x15, x15, valid8 # expected: x15=x16=69
jal x1, error

valid8:
addi x15, x15, 1   # a5 = 70, a6 = 69
bne x15, x16, valid9
jal x1, error

valid9:
li x16, -1         # a6
bgt x15, x16, valid10
jal x1, error

valid10:
bltu x15, x16, valid11
jal x1, error

valid11:
bgeu x16, x15, valid12
jal x1, error

valid12:
blt x16, x15, valid13
jal x1, error

valid13:
bltu x16, x15, error
jal x1, exit

procedure:
li x15, 69         # a5
li x16, 69         # a6
jalr x1, 0(x1)     # return

error:
li x17, -1         # a7 = -1

exit:
nop

li x5, 0x10010000
sw x0, 0(x5)
sw x1, 4(x5)
sw x2, 8(x5)
sw x3, 12(x5)
sw x4, 16(x5)
sw x5, 20(x5)
sw x6, 24(x5)
sw x7, 28(x5)
sw x8, 32(x5)
sw x9, 36(x5)
sw x10, 40(x5)
sw x11, 44(x5)
sw x12, 48(x5)
sw x13, 52(x5)
sw x14, 56(x5)
sw x15, 60(x5)
sw x16, 64(x5)
sw x17, 68(x5)
sw x18, 72(x5)
sw x19, 76(x5)
sw x20, 80(x5)
sw x21, 84(x5)
sw x22, 88(x5)
sw x23, 92(x5)
sw x24, 96(x5)
sw x25, 100(x5)
sw x26, 104(x5)
sw x27, 108(x5)
sw x28, 112(x5)
sw x29, 116(x5)
sw x30, 120(x5)
sw x31, 124(x5)
