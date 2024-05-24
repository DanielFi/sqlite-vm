PUSH[5]
CALL[sum] ; sum(5)
FIN

; sum(N)
sum:
PICK[1]
DUP
JUMPZ[sumret]
DUP
PUSH[1]
SUB
CALL[sum] ; sum(N-1)
ADD
sumret:
PICK[1]
RET