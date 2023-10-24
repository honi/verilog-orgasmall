import re
from pathlib import Path

from isa import *


def assemble_program(filename):
    basedir = Path(__file__).resolve().parent / "programs"
    with open(basedir / filename) as f:
        asm = f.read()

    # Dividimos el programa por líneas y descartamos las líneas vacías.
    lines = [
        line.strip()
        for line in re.sub(r":\s+", ":", asm).strip().split("\n")
        if line.strip() and not re.match(r"^(#|\/\/)", line.strip())
    ]

    # Primera pasada: calculamos las etiquetas.
    label_to_addr = {}
    for addr, line in enumerate(lines):
        if ":" in line:
            label, inst = line.split(":")
            label_to_addr[label.strip().upper()] = addr
            lines[addr] = inst.strip()

    # Segunda pasada: codificamos el programa.
    program = []
    for line in lines:
        tokens = re.split(r"[\s,]+", line.upper())

        # Primero siempre viene el nombre de la instrucción.
        i = 0
        opname = tokens[i]
        i += 1

        # Validamos el opname.
        opcode = None
        type = None
        if opname != "DW":
            try:
                opcode = INSTRUCTIONS[opname]["opcode"]
                type = INSTRUCTIONS[opname]["type"]
            except KeyError:
                raise Exception(f"Invalid instruction name: {line}")

        # Extraemos los operandos.
        rx = None
        ry = None
        imm = None

        if type in ["A", "B", "D"]:
            try:
                rx = tokens[i]
                i += 1
            except IndexError:
                raise Exception(f"Missing RX operand: {line}")

        if type in ["A"]:
            try:
                ry = tokens[i]
                i += 1
            except IndexError:
                raise Exception(f"Missing RY operand: {line}")

        if type in ["C", "D"] or opname == "DW":
            try:
                imm = tokens[i]
                i += 1
            except IndexError:
                raise Exception(f"Missing immediate operand: {line}")

        # Validamos los operandos.
        if rx is not None:
            mx = re.match(r"R([0-7])", rx)
            if not mx:
                raise Exception(f"Invalid RX operand: {line}")
            rx = int(mx.groups(1)[0])

        if ry is not None:
            my = re.match(r"R([0-7])", ry)
            if not my:
                raise Exception(f"Invalid RY operand: {line}")
            ry = int(my.groups(1)[0])

        if imm is not None:
            if imm in label_to_addr:
                imm = label_to_addr[imm]
            else:
                try:
                    if "0X" in imm:
                        imm = int(imm[2:], 16)
                    else:
                        imm = int(imm)
                except ValueError:
                    raise Exception(f"Invalid immediate operand: {line}")

        # Codificamos la instrucción.
        if opname == "DW":
            program.append(imm)
        else:
            program.append(encode(opcode, rx=rx, ry=ry, imm=imm))

    return program
