li x10, 0x04038101       # Simulator has a bug and loads 0x04039101 = 67342593
sw x10, 0(x0)           # Expected values
lw x11, 0(x0)           # x11 = 67342593
lh x12, 0(x0)           # x12 = -28415
lh x13, 2(x0)           # x13 = 1027
lb x14, 0(x0)           # x14 = 1
lb x15, 1(x0)           # x15 = -111
lb x16, 2(x0)           # x16 = 3
lb x17, 3(x0)           # x17 = 4
lhu x12, 0(x0)          # x12 = 37129
lhu x13, 2(x0)          # x13 = 1027
lbu x14, 0(x0)          # x14 = 1
lbu x15, 1(x0)          # x15 = 145
lbu x16, 2(x0)          # x16 = 3
lbu x17, 3(x0)          # x17 = 4
sh x12, 4(x0)           # Store halfword at address 4
sh x13, 6(x0)           # 2*sh =sw
sb x14, 8(x0)           # Store byte at address 8
sb x15, 9(x0)           # Store byte at address 9
sb x16, 10(x0)          # Store byte at address 10
sb x17, 11(x0)          # 4*sb =sw
beq x10, x11, valid     # Branch if x10 == x11
jal x0, error           # Jump to error
valid: 
  jal x0, exit          # Jump to exit
error: 
  li x10, -1            # Load -1 into x10
exit: 
  nop                   # No operation
