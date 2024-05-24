from argparse import ArgumentParser
from pathlib import Path
import re
import sqlite3


OPCODES = {
    'NOP': 0,
    'PUSH': 1,
    'POP': 2,
    'DUP': 4,
    'PICK': 5,
    'ADD': 6,
    'SUB': 8,
    'AND': 10,
    'OR': 12,
    'NOT': 14,
    'JUMP': 15,
    'JUMPP': 16,
    'RET': 16,
    'JUMPZ': 17,
    'JUMPPZ': 18,
    'CALL': 19,
    'CALLP': 20,
    'READ': 22,
    'WRITE': 24,
    'PUTC': 26,
    'FIN': 254
}


def assemble(assembly: str) -> bytes:
    assembly_pattern = re.compile(r'^\s*(?:(\w+)(\[(?:\d+|\w+)\])?)?\s*(?:;.*)?$')
    label_pattern = re.compile(r'^\s*([a-zA-Z]+):\s*(?:;.*)?$')

    lines = [line.strip() for line in assembly.splitlines(keepends=False)]

    labels = {}
    offset = 0
    for line in lines:
        match = assembly_pattern.match(line)
        if match is not None:
            if match.group(2) is not None:
                offset += 2
            elif match.group(1) is not None:
                offset += 1
            
            continue
        
        match = label_pattern.match(line)
        if match is not None:
            labels[match.group(1)] = offset

    result = []

    for i, line in enumerate(lines):
        if not line:
            continue
        
        match = assembly_pattern.match(line)

        if not match:
            if label_pattern.match(line):
                continue
            raise ValueError(f'Invalid assembly at line {i}')


        mnemonic = match.group(1)

        if not mnemonic:
            continue

        if mnemonic not in OPCODES:
            raise ValueError(f'Unknown opcode "{mnemonic}"')

        result.append(OPCODES[mnemonic])

        arg = match.group(2)
        if arg is not None:
            arg = arg[1:-1]
            if arg.isalpha():
                try:
                    arg = labels[arg]
                except KeyError:
                    raise ValueError(f'Invalid label {arg}')
            else:
                arg = int(arg, base=0)
                if arg > 256 or arg < -255:
                    raise ValueError(f'Invalid arg value {arg}')
            result.append(arg)

    return bytes(result)


def serialize_program(program: bytes, output_path: str):
    Path(output_path).unlink(missing_ok=True)
    conn = sqlite3.connect(output_path)
    conn.execute('CREATE TABLE program(program BLOB);')
    conn.execute(f'INSERT INTO program VALUES(?);', (program,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()

    program = assemble(Path(args.input).read_text())
    serialize_program(program, args.output)
