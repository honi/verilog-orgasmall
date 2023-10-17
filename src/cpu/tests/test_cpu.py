import sys
import cocotb
from cocotb.triggers import RisingEdge, Timer, ClockCycles
from cocotb.clock import Clock
from cocotb.types import LogicArray, Range

sys.path.append("../../shared/tests")
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


@cocotb.test()
async def test_add(dut):
    await run_program(dut, [
        encode(OPCODES["SET"], rx=1, imm=42),
        encode(OPCODES["SET"], rx=2, imm=58),
        encode(OPCODES["ADD"], rx=1, ry=2),
    ])
    assert dut.registers.data[1].value == 100

# @cocotb.test()
# async def test_adc(dut):
#     await test_op(dut, OPCODES["ADC"], 1, 2, op_ADC(1, 2))

# @cocotb.test()
# async def test_sub(dut):
#     await test_op(dut, OPCODES["SUB"], 5, 1, op_SUB(5, 1))

# @cocotb.test()
# async def test_and(dut):
#     await test_op(dut, OPCODES["AND"], 0xFFFF, 0x1234, op_AND(0xFFFF, 0x1234))

# @cocotb.test()
# async def test_or(dut):
#     await test_op(dut, OPCODES["OR"], 0xF0F0, 0x0F0F, op_OR(0xF0F0, 0x0F0F))

# @cocotb.test()
# async def test_xor(dut):
#     await test_op(dut, OPCODES["XOR"], 0b1010, 0b0110, op_XOR(0b1010, 0b0110))

# @cocotb.test()
# async def test_cmp(dut):
#     await test_op(dut, OPCODES["CMP"], 666, 666, op_CMP(666, 666))
#     await test_op(dut, OPCODES["CMP"], 1, 7, op_CMP(1, 7))

# @cocotb.test()
# async def test_inc(dut):
#     await test_op(dut, OPCODES["INC"], 42, 0, op_INC(42))

# @cocotb.test()
# async def test_dec(dut):
#     await test_op(dut, OPCODES["DEC"], 42, 0, op_DEC(42))

# @cocotb.test()
# async def test_shr(dut):
#     await test_op(dut, OPCODES["SHR"], 8, 2, op_SHR(8, 2))

# @cocotb.test()
# async def test_shl(dut):
#     await test_op(dut, OPCODES["SHL"], 8, 2, op_SHL(8, 2))
