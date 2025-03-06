import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('file', help='name of the assembly file to assemble.')
parser.add_argument('-d', '--destination', help='destination file for the machine code.')
cmdargs = parser.parse_args()

class Instruction:

    def __init__(self, line):
        self.op = None
        self.rs1 = None
        self.rs2 = None
        self.rd = None
        self.imdt = None

        reg_groups = [
            ('operation', r'^[A-Za-z]+'),
            ('registerX', r'[Xx][0-9][0-9]?'),
            ('registerT', r'[Tt][0-6]'),
            ('registerA', r'[Aa][0-7]'),
            ('registerS', r'[Ss][0-9][0-9]?'),
            ('registerP', r'[SsGgTtFf][Pp]'),
            ('registerRA', r'[Rr][Aa]'),
            ('register0', r'[Zz][Ee][Rr][Oo]'),
            ('immediate', r'-?\d+')
        ]
        line = str(line).split('#', 1)[0].strip()
        tokens = []
        for match in re.finditer('|'.join('(?P<%s>%s)' % group for group in reg_groups), line):
            if match.group() != '':
                tokens.append((match.lastgroup, match.group()))
        for idx, token in enumerate(tokens):
            match token[0]:
                case 'registerX':
                    tokens[idx] = int(re.split(r'[Xx]', token[1], maxsplit=1)[1])
                case 'registerT':
                    t = int(re.split(r'[Tt]', token[1], maxsplit=1)[1])
                    tokens[idx] = 5 + t if t <= 2 else 28 + t - 3
                case 'registerA':
                    a = int(re.split(r'[Aa]', token[1], maxsplit=1)[1])
                    tokens[idx] = 10 + a
                case 'registerS':
                    s = int(re.split(r'[Ss]', token[1], maxsplit=1)[1])
                    tokens[idx] = 8 + s if s <= 1 else 18 + s - 2
                case 'registerP':
                    p = re.split(r'[Pp]', token[1], maxsplit=1)[0].lower()
                    tokens[idx] = 2 if p == 's' else 3 if p =='g' else 4 if p == 't' else 8
                case 'registerRA':
                    tokens[idx] = 1
                case 'register0':
                    tokens[idx] = 0
                case 'immediate':
                    tokens[idx] = int(token[1])
        if len(tokens) >= 1 and tokens[0][0] == 'operation':
            self.op = tokens[0][1].lower()
            match self.op:
                case 'add':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.rs2 = tokens[3]
                case 'addi':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.imdt = tokens[3]
                case 'sll': 
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.rs2 = tokens[3]
                case 'slli':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.imdt = tokens[3]
                case 'srl':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.rs2 = tokens[3]
                case 'srli':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.imdt = tokens[3]
                case 'xor':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.rs2 = tokens[3]
                case 'ori':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.imdt = tokens[3]
                case 'andi':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.imdt = tokens[3]
                case 'mul':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.rs2 = tokens[3]
                case 'beq':
                    self.rs1 = tokens[1]
                    self.rs2 = tokens[2]
                    self.imdt = tokens[3]
                case 'bne':
                    self.rs1 = tokens[1]
                    self.rs2 = tokens[2]
                    self.imdt = tokens[3]

class Program:
    def __init__(self, code):
        self.ins = list()
        
        for line in code.splitlines():
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            instruction = Instruction(line)
            if instruction.op is not None:
                self.ins.append(instruction)

    def assemble(self, f):
        for line in self.ins:
            if not line.op in ['add', 'addi', 'sll', 'slli', 'srl', 'srli', 'xor', 'ori', 'andi', 'mul', 'beq', 'bne']:
                continue
            bits = int()
            # assemble
            if line.op in ['add', 'sll', 'srl', 'xor', 'mul']:
                opcode = 0b0110011
                rd = (line.rd & 0b11111) << 7
                func3 = 0b000 << 12
                rs1 = (line.rs1 & 0b11111) << 15
                rs2 = (line.rs2 & 0b11111) << 20
                func7 = 0b0000000 << 25
                match line.op:
                    case 'add':
                        pass
                    case 'sll':
                        func3 = 0b001 << 12
                    case 'srl':
                        func3 = 0b101 << 12
                    case 'xor':
                        func3 = 0b100 << 12
                    case 'mul':
                        func7 = 0b0000001 << 25
                bits = opcode | rd | func3 | rs1 | rs2 | func7
            elif line.op.endswith('i'):
                opcode = 0b0010011
                rd = (line.rd & 0b11111) << 7
                func3 = 0b000 << 12
                rs1 = (line.rs1 & 0b11111) << 15
                imdt = (line.imdt & 0xFFF) # << 20
                if imdt & 0x800:
                    imdt = imdt | 0xFFFFF000
                imdts = imdt << 20
                match line.op:
                    case 'addi':
                        pass
                    case 'slli':
                        func3 = 0b001 << 12
                    case 'srli':
                        func3 = 0b101 << 12
                    case 'ori':
                        func3 = 0b110 << 12
                    case 'andi':
                        func3 = 0b111 << 12
                bits = opcode | rd | func3 | rs1 | imdts
            elif line.op in ['beq', 'bne']:
                # bits_imdt = [line.imdt >> i & 1 for i in range(line.imdt.bit_length() - 1,-1,-1)]
                # bits_imdt.reverse()
                
                # bits_imdt_14 = bits_imdt[1:4]
                # bits_imdt_14.reverse()
                # imdt1 = int('0b'+str(bits_imdt_14)+str(bits_imdt[11]), base=0) << 7

                opcode = 0b1100011
                func3 = 0b000 << 12 if line.op == 'beq' else 0b001 << 12
                rs1 = (line.rs1 & 0b11111) << 15
                rs2 = (line.rs2 & 0b11111) << 20
                
                bit7_imdt11 = (line.imdt & 0x800) >> 4 # now at bit 7
                bit11_8_imdt4_1 = (line.imdt & 0x1E) << 7 # now at bit 8-11
                bit_30_25_imdt10_5 = (line.imdt & 0x7E0) << 20 # now at bit 25-30
                bit_31_imdt12 = (line.imdt & 0x1000) << 19 # now at bit 31
                # bits_imdt_510 = bits_imdt[10:5]
                # bits_imdt_510.reverse()
                # imdt2 = int('0b'+str(bits_imdt[12]+str(bits_imdt_510)), base=0) << 25
                bits = opcode | bit7_imdt11 | bit11_8_imdt4_1 | func3 | rs1 | rs2 | bit_30_25_imdt10_5 | bit_31_imdt12
            # export to f
            f.write(f'{hex(bits)}\n')
            

if __name__ == '__main__':
    print(f'assembling file {cmdargs.file}')
    with open(cmdargs.file, 'r', encoding="utf-8") as src:
        code = src.read()
        p = Program(code)
        for ins in p.ins:
            print(f'op: {ins.op}, rd: {ins.rd}, rs1: {ins.rs1}, rs2: {ins.rs2}, imdt: {ins.imdt}\n', end='')
        desname = cmdargs.destination if cmdargs.destination else (cmdargs.file.split('.', maxsplit=1)[0]+'.mc')
        with open(desname, 'w', encoding="utf-8") as des:
            p.assemble(des)
            print(f'machine code written to {desname}\n')
    