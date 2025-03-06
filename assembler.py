import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='name of the assembly file to assemble.')
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
            ('immediate', r'-?\d*')
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
        if tokens[0][0] == 'operation':
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
                # TO-DO
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
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.imdt = tokens[3]
                case 'bne':
                    self.rd = tokens[1]
                    self.rs1 = tokens[2]
                    self.imdt = tokens[3]

class Program:
    def __init__(self, code):
        self.register = [0] * 32
        self.ins = list()
        self.pc = int(0)
        
        for line in code.splitlines():
            self.ins.append(Instruction(line))

    def assemble(f):
        pass

if __name__ == '__main__':
    print(f'assembling file {cmdargs.file}')
    with open(cmdargs.file, 'r', encoding="utf-8") as f:
        code  = f.read()
        p = Program(code)
        for ins in p.ins:
            print(f'op: {ins.op}, rd: {ins.rd}, rs1: {ins.rs1}, rs2: {ins.rs2}, imdt: {ins.imdt}\n', end='')