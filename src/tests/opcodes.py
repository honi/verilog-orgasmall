ADD = 0b00001
ADC = 0b00010
SUB = 0b00011
AND = 0b00100
OR = 0b00101
XOR = 0b00110
CMP = 0b00111
MOV = 0b01000
STR = 0b10000
LOAD = 0b10001
RSTR = 0b10010
RLOAD = 0b10011
JMP = 0b10100
JC = 0b10101
JZ = 0b10110
JN = 0b10111
INC = 0b11000
DEC = 0b11001
SHR = 0b11010
SHL = 0b11011
SET = 0b11111

def op_ADD(x, y): return x + y
def op_ADC(x, y): return x + y
def op_SUB(x, y): return x - y
def op_AND(x, y): return x & y
def op_OR(x, y): return x | y
def op_XOR(x, y): return x ^ y
def op_CMP(x, y): return bool(x == y)
def op_INC(x): return x + 1
def op_DEC(x): return x - 1
def op_SHR(x, y): return x >> y
def op_SHL(x, y): return x << y

OPFUNCS = {
    ADD: op_ADD,
    ADC: op_ADC,
    SUB: op_SUB,
    AND: op_AND,
    OR: op_OR,
    XOR: op_XOR,
    CMP: op_CMP,
    INC: op_INC,
    DEC: op_DEC,
    SHR: op_SHR,
    SHL: op_SHL,
}