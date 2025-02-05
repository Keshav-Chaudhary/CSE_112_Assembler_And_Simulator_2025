addi a0,zero,-5
add a0,zero,zero
beq zero,zero,0
lw s2,0(s1)
jalr s2,s1,16
sw s2,0(s0)
bgeu s0,s1,96