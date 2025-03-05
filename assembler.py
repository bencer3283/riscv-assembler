import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='name of the assembly file to assemble.')
cmdargs = parser.parse_args()

if __name__ == '__main__':
    print(f'assembling file {cmdargs.file}')
    with open(cmdargs.file, 'r', encoding="utf-8") as f:
        code  = f.read()
        for line in code.splitlines():
            print(f'{line}\n', end='')