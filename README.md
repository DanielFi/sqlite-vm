# SQLite VM

A simple 8-bit stack VM implementation in SQLite.  

All SQL is hand written in `emulator.sql`.  
Programs are stored as SQLite database files and can be created with `assembler.py`.  
Samples programs can be found in `examples/`.  

## Usage

Assemble a program:
```sh
python3 assembler.py examples/hello.asm examples/hello.db
```

And run it:

```sh
./emulator.sh examples/hello.db
```

## I/O

The `PUTC` instruction outputs a character to STDOUT using SQLite's fileio
extension, by writing to `/proc/self/fd/1`.

> The fileio extension should be compiled into the sqlite3 binary by default.

## Architecture

* 8-bit
* stack based (no registers)
* unlimited stack
* 256 bytes program memory
* 256 bytes RAM

### Instruction Set

#### 0 - NOP

#### 1 - PUSH[x]
stack: `       ->  x`

#### 2 - POP
stack: `_      ->  `

#### 4 - DUP
stack: `x      ->  x x`

#### 5 - PICK[n]
stack: `x0 x1 ... xn   -> x1 ... xn x0`

#### 6 - ADD
stack: `x y ->  x+y`

#### 8 - SUB
stack: `x y ->  x-y`

#### 10 - AND
stack: `x y ->  x&y`

#### 12 - OR
stack: `x y ->  x|y`

#### 14 - NOT
stack: `x   ->  ~x`

#### 15 - JUMP[x]
pc: `x`

#### 16 - JUMPP/RET
stack: `x   ->  `  
pc: `x`

#### 17 - JUMPZ[x]
stack: `c   ->  `  
pc: if `c=0`, `x`

#### 18 - JUMPPZ
stack: `c x ->  `  
pc: if `c=0`, `x`

#### 19 - CALL[x]
stack: `    -> pc + 2`
pc: `x`

#### 20 - CALLP
stack: `x   -> pc + 1`
pc: `x`

#### 22 - READ
stack: `i   -> memory[i]`

#### 24 - WRITE
stack: `x i ->  `
memory: `[i] = x`

#### 26 - PUTC
stack: `c   ->  `

#### 254 - FIN
