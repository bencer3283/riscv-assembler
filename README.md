# RISC-V Assembler

A Python-based assembler for RISC-V architecture.

## Installation

This project uses a conda environment. To set up:

```bash
# Create the conda environment from env.yml
conda env create -f env.yml

# Activate the environment
conda activate riscv-assembler
```

## Command Line Interface

```
python assembler.py <input_file> [-d <output_file>]
```

### Arguments

- `input_file`: Path to the RISC-V assembly file (`.s` extension)
- `-d, --destination`: (Optional) Path to output machine code file. If not specified, machine code will be stored in a `.mc` file with the same name as the input file.

## Supported Instructions

### R-type Instructions
- `add rd, rs1, rs2`
- `sll rd, rs1, rs2`
- `srl rd, rs1, rs2`
- `xor rd, rs1, rs2`
- `mul rd, rs1, rs2`

### I-type Instructions
- `addi rd, rs1, imm`
- `slli rd, rs1, imm`
- `srli rd, rs1, imm`
- `ori rd, rs1, imm`
- `andi rd, rs1, imm`

### B-type Instructions
- `beq rs1, rs2, offset`
- `bne rs1, rs2, offset`

## Register Names

The assembler supports both standard RISC-V register names and ABI names:

- `x0` to `x31`: Standard registers
- ABI names: `zero`, `ra`, `sp`, `gp`, `tp`, `t0`-`t6`, `s0`-`s11`, `a0`-`a7`, `fp`