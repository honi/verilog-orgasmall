// Guardamos desde 0xF0 los números: 1, 2, 3, 4.
SET R0, 1
STR R0, 0xF0
SET R0, 2
STR R0, 0xF1
SET R0, 3
STR R0, 0xF2
SET R0, 4
STR R0, 0xF3

SET R0, 0xF0 # Dirección base
SET R1, 0    # Acumulador
SET R2, 4    # Elementos restantes

loop:
RLOAD R7, R0 # R7 <- Mem[R0]
ADD R1, R7   # Acumulamos el elemento
INC R0       # Incrementamos la dirección al próximo elemento
DEC R2       # Restamos 1 a los elementos restantes
JZ halt
JMP loop

halt:
JMP halt
