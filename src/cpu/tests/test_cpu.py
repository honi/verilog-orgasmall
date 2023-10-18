import sys
import cocotb
from cocotb.triggers import RisingEdge, Timer, ClockCycles
from cocotb.clock import Clock
from cocotb.types import LogicArray, Range

sys.path.append("../../shared/tests")
from config import *
from opcodes import *


async def run_program(dut, program):
    # Cargamos el programa en memoria.
    for addr, inst in enumerate(program):
        dut.inst_memory.data[addr].value = inst

    # Configuramos el clock y nos sincronizamos.
    clock = Clock(dut.clk, 10, "us")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)

    # Reset cycle.
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # Single-cycle for the win!
    # Necesitamos len(program) ciclos para ejecutar todo el programa.
    await ClockCycles(dut.clk, len(program))


def encode(opcode, rx=None, ry=None, imm=None):
    inst_hi = opcode << 3
    inst_lo = 0

    if rx is not None: inst_hi |= rx
    if ry is not None: inst_lo |= ry << 5
    if imm is not None: inst_lo = imm

    return (inst_hi << 8) | inst_lo


async def test_op(dut, opcode, *operands):
    await run_program(dut, [
        encode(SET, rx=1, imm=operands[0] if len(operands) >= 1 else 0),
        encode(SET, rx=2, imm=operands[1] if len(operands) >= 2 else 0),
        encode(opcode, rx=1, ry=2),
    ])
    expected = OPFUNCS[opcode](*operands)
    assert dut.registers.data[1].value == expected, f"{int(dut.registers.data[1].value)} != {expected}"


@cocotb.test()
async def test_add(dut):
    await test_op(dut, ADD, 1, 2)

@cocotb.test()
async def test_adc(dut):
    await test_op(dut, ADC, 1, 2)

@cocotb.test()
async def test_sub(dut):
    await test_op(dut, SUB, 5, 1)

@cocotb.test()
async def test_and(dut):
    await test_op(dut, AND, 0xFF, 0x12)

@cocotb.test()
async def test_or(dut):
    await test_op(dut, OR, 0xF0, 0x0F)

@cocotb.test()
async def test_xor(dut):
    await test_op(dut, XOR, 0b1010, 0b0110)

@cocotb.test()
async def test_cmp(dut):
    await test_op(dut, CMP, 120, 120)
    await test_op(dut, CMP, 1, 7)

@cocotb.test()
async def test_inc(dut):
    await test_op(dut, INC, 42)

@cocotb.test()
async def test_dec(dut):
    await test_op(dut, DEC, 42)

@cocotb.test()
async def test_shr(dut):
    await test_op(dut, SHR, 8, 2)

@cocotb.test()
async def test_shl(dut):
    await test_op(dut, SHL, 8, 2)

@cocotb.test()
async def test_set(dut):
    await run_program(dut, [
        encode(SET, rx=i, imm=100 + i)
        for i in range(NUM_REGISTERS)
    ])
    for i in range(NUM_REGISTERS):
        assert dut.registers.data[i].value == 100 + i
