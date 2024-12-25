li s0, 0
begin: 
  beq s0, x0, start
  jal x0, exit
start:
li x5, 0x10010000
li x10, 0x04038101       # Simulator has a bug and loads 0x04039101 = 67342593
sw x10, 0(x5)           # Expected values
lw x11, 0(x5)           # x11 = 67342593
lh x12, 0(x5)           # x12 = -28415
lh x13, 8(x5)           # x13 = 1027
lb x14, 0(x5)           # x14 = 1
lb x15, 4(x5)           # x15 = -111
lb x16, 8(x5)           # x16 = 3
lb x17, 12(x5)           # x17 = 4
lhu x12, 0(x5)          # x12 = 37129
lhu x13, 8(x5)          # x13 = 1027
lbu x14, 0(x5)          # x14 = 1
lbu x15, 4(x5)          # x15 = 145
lbu x16, 8(x5)          # x16 = 3
lbu x17, 12(x5)          # x17 = 4
sh x12, 16(x5)           # Store halfword at address 4
sh x13, 24(x5)           # 2*sh =sw
sb x14, 32(x5)           # Store byte at address 8
sb x15, 36(x5)           # Store byte at address 9
sb x16, 40(x5)          # Store byte at address 10
sb x17, 44(x5)          # 4*sb =sw
beq x10, x11, valid     # Branch if x10 == x11
jal x0, error           # Jump to error
valid: 
  jal x0, exit          # Jump to exit
  li s0, 1
error: 
  li x10, -1            # Load -1 into x10
  j begin
exit: 
  nop                   # No operation


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
