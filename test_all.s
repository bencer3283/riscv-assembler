# Test for all registers and instructions
# Register test
addi x0, x0, 0    # zero register
addi x1, x0, 1    # ra register
addi x2, x0, 2    # sp register
addi x3, x0, 3    # gp register
addi x4, x0, 4    # tp register
addi x5, x0, 5    # t0 register
addi x6, x0, 6    # t1 register
addi x7, x0, 7    # t2 register
addi x8, x0, 8    # s0/fp register
addi x9, x0, 9    # s1 register
addi x10, x0, 10  # a0 register
addi x11, x0, 11  # a1 register
addi x12, x0, 12  # a2 register
addi x13, x0, 13  # a3 register
addi x14, x0, 14  # a4 register
addi x15, x0, 15  # a5 register
addi x16, x0, 16  # a6 register
addi x17, x0, 17  # a7 register
addi x18, x0, 18  # s2 register
addi x19, x0, 19  # s3 register
addi x20, x0, 20  # s4 register
addi x21, x0, 21  # s5 register
addi x22, x0, 22  # s6 register
addi x23, x0, 23  # s7 register
addi x24, x0, 24  # s8 register
addi x25, x0, 25  # s9 register
addi x26, x0, 26  # s10 register
addi x27, x0, 27  # s11 register
addi x28, x0, 28  # t3 register
addi x29, x0, 29  # t4 register
addi x30, x0, 30  # t5 register
addi x31, x0, 31  # t6 register

# ABI name test
addi zero, zero, 0
addi ra, zero, 1
addi sp, zero, 2
addi gp, zero, 3
addi tp, zero, 4
addi t0, zero, 5
addi t1, zero, 6
addi t2, zero, 7
addi fp, zero, 8
addi s1, zero, 9
addi a0, zero, 10
addi a1, zero, 11
addi a2, zero, 12
addi a3, zero, 13
addi a4, zero, 14
addi a5, zero, 15
addi a6, zero, 16
addi a7, zero, 17
addi s2, zero, 18
addi s3, zero, 19
addi s4, zero, 20
addi s5, zero, 21
addi s6, zero, 22
addi s7, zero, 23
addi s8, zero, 24
addi s9, zero, 25
addi s10, zero, 26
addi s11, zero, 27
addi t3, zero, 28
addi t4, zero, 29
addi t5, zero, 30
addi t6, zero, 31

# Operation test
add a0, a1, a2       # add test
addi a0, a1, 42      # addi test with positive immediate
addi a0, a1, -42     # addi test with negative immediate
sll a0, a1, a2       # sll test
slli a0, a1, 5       # slli test
srl a0, a1, a2       # srl test
srli a0, a1, 5       # srli test
xor a0, a1, a2       # xor test
ori a0, a1, 42       # ori test
andi a0, a1, 42      # andi test
mul a0, a1, a2       # mul test

# Branch test with direct line numbers as branch targets
addi a0, zero, 5     # Line 82
addi a1, zero, 5     # Line 83
beq a0, a1, 85       # Line 84: branch to line 85
addi a2, zero, 99    # Line 85: skipped if the branch is taken

addi a3, zero, 10    # Line 86
addi a4, zero, 20    # Line 87
bne a3, a4, 90       # Line 88: branch to line 90
addi a5, zero, 99    # Line 89: skipped if the branch is taken

addi a6, zero, 42    # Line 90