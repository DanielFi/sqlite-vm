PUSH[5]
CALL[sum]
FIN

; sum(N): sum all numbers from 1 to N
sum:
PUSH[0]
PICK[2]

sumloop:
DUP
PICK[2]
ADD
PICK[1]

PUSH[1]
SUB

DUP
JUMPZ[sumret]
JUMP[sumloop]

sumret:
POP
PICK[1]
RET
