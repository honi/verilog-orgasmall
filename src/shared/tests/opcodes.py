from os import path


OPCODES = {}
with open(path.join(path.dirname(__file__), "../opcodes.gtkw")) as f:
    for line in f.readlines():
        opcode, opname = line.strip().split(" ")
        OPCODES[opname] = int(opcode, 2)


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