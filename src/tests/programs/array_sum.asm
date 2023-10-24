// Guardamos desde 0xF0 los números: 1, 2, 3, 4.
SET R0, 0x01
STR R0, 0xF0
SET R0, 0x02
STR R0, 0xF1
SET R0, 0x03
STR R0, 0xF2
SET R0, 0x04
STR R0, 0xF3

SET R0, 0xF0 # Dirección base
SET R1, 1 # Constante 1
SET R3, 0 # Acumulador
SET R6, 4 # Elementos restantes

loop:
RLOAD R2, R0 # R2 <- Mem[R0]
ADD R3, R2 # Acumulamos el elemento
ADD R0, R1 # Incrementamos la dirección al próximo elemento
SUB R6, R1 # Restamos 1 a los elementos restantes
JZ halt
JMP loop

halt:
JMP halt
