import cocotb
from cocotb.triggers import Timer
from cocotb.types import LogicArray, Range

from config import *
from isa import *
from runner import test_module


async def test_op(dut, opcode, *operands):
    dut.a.value = operands[0] if len(operands) >= 1 else 0
    dut.b.value = operands[1] if len(operands) >= 2 else 0
    dut.opcode.value = opcode
    await Timer(10, "us")
    expected = OPFUNCS[opcode](*operands)
    assert LogicArray(dut.out.value) == LogicArray(expected, Range(WORD_SIZE-1, 'downto', 0))


@cocotb.test()
async def test_add(dut):
    await test_op(dut, ADD, 1, 2)

@cocotb.test()
async def test_adc(dut):
    await test_op(dut, ADC, 1, 2)

@cocotb.test()
async def test_sub(dut):
    await test_op(dut, SUB, 5, 1)
    await test_op(dut, SUB, 1, 5)

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
    await test_op(dut, CMP, 100, 100)
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


if __name__ == "__main__":
    test_module("alu")
