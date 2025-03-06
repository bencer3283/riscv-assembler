import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='name of the assembly file to assemble.')
cmdargs = parser.parse_args()

class Instruction:
    # op: str
    # rs1: int
    # rs2: int
    # rd: int
    # imdt: int

    def __init__(self, line):
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
        self.tokens = []
        for match in re.finditer('|'.join('(?P<%s>%s)' % group for group in reg_groups), line):
            if match.group() != '':
                self.tokens.append({match.lastgroup: match.group()})

if __name__ == '__main__':
    print(f'assembling file {cmdargs.file}')
    with open(cmdargs.file, 'r', encoding="utf-8") as f:
        code  = f.read()
        for line in code.splitlines():
            ins = Instruction(line)
            print(f'op: {ins.tokens}\n', end='')