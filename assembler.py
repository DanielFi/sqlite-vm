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
    'JUMPZ': 17,
    'JUMPPZ': 18,
    'PC': 20,
    'FIN': 254
}


def assemble(assembly: str) -> bytes:
    pattern = re.compile(r'(?:(\w+)(\[\d+\])?)?\s*(?:;.*)?')

    result = []

    for i, line in enumerate(assembly.splitlines(keepends=False)):
        line = line.strip()
        if not line:
            continue
        
        match = pattern.match(line)

        if not match:
            raise ValueError(f'Invalid assembly at line {i}')

        mnemonic = match.group(1)

        if not mnemonic:
            continue

        if mnemonic not in OPCODES:
            raise ValueError(f'Unknown opcode "{mnemonic}"')

        result.append(OPCODES[mnemonic])

        arg = match.group(2)
        if arg is not None:
            arg = int(arg[1:-1], base=0)
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
