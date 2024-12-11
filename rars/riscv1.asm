li x7, 1
li x1, 15
li x2, -5
li x3,  5
add x4, x1, x2 
sub x5, x1, x3 # expected- x4=x5=10
addi x6, x6, 0 # test with no stall
beq x5, x4, valid0  # tested- add, addi, sub, beq, jal
jal error
valid0: auipc x4, 1
lui x5, 1
addi x5, x5, 36 # expected- x4=x5=4128
beq x5, x4, valid1  # tested- lui, auipc
jal error
valid1: li x0, 0xc
li x1, 0xa
and x2, x1, x0
or x3, x1, x0
li x4, 0x6
xor x5, x3, x4 # expected- x2=x5=8
beq x2, x5, valid2  # tested- and, or, xor
jal error
valid2: andi x2, x0, 0xa
ori x3, x0, 0xa
xori x5, x3, 0x6 # expected- x2=x5=8
beq x2, x5, valid3  # tested- andi, ori, xori
jal error
valid3: li x0, 1
li x1, -1
slt x2, x0, x1
sltu x3, x0, x1
addi x2, x2, 1 # expected- x2=x3=1
beq x2, x3, valid4  # tested- slt, sltu
jal error
valid4: slti x2, x0, -1
sltiu x3, x0, -1
addi x2, x2, 1 # expected- x2=x3=1
beq x2, x3, valid5  # tested- slti, sltiu
jal error
valid5: li x1, 2
sll x2, x0, x1
srl x2, x2, x0
slli x3, x0, 2
srli x3, x3, 1 # expected- x2=x3=2
beq x2, x3, valid6  # tested- sll, srl, slli, srli
jal error
valid6: li x0, -8
li x4, 2
srai x2, x0, 2
sra x3, x0, x4 # expected- x2=x3=-2
beq x2, x3, valid7  # tested- sra, srai
jal error
valid7: jal procedure # expected- x5=x6=69
beq x5, x6, valid8  # tested- jal, jalr
jal error
valid8: addi x6, x6, 1 # expected- x5=70 x6=69
bne x5, x6, valid9  # tested- bne
jal error
valid9: li x6, -1 # expected- x5=69 x6=-1 (for next 4 branches)
bgt x5, x6, valid10  # tested- gt
jal error
valid10: bltu x5, x6, valid11  # tested- ltu
jal error
valid11: bgeu x6, x5, valid12  # tested- ltu
jal error
valid12: blt x6, x5, valid13  # tested- ltu
jal error
valid13: bltu x6, x5, error  # tested- ltu
jal exit
procedure: li x5, 69
li x6, 69
jalr x1, 0(x1)  # return
error: li x7, -1 
exit: nop
