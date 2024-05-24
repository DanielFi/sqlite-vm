PUSH[5]
CALL[5]
FIN

; 5 | sum(N): sum all numbers from 1 to N
PUSH[0]
PICK[2]

; 9 |
DUP
PICK[2]
ADD
PICK[1]

PUSH[1]
SUB

DUP
JUMPZ[23]
JUMP[9]

; 23 |
POP
PICK[1]
RET
