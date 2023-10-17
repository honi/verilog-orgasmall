import sys
import cocotb
from cocotb.triggers import Timer

sys.path.append("../../shared/tests")
from opcodes import *

async def test_op(dut, opcode, a, b, expected):
    dut.a.value = a
    dut.b.value = b
    dut.opcode.value = opcode
    await Timer(10, "us")
    assert dut.out.value == expected, f"{int(dut.out.value)} != {expected}"


@cocotb.test()
async def test_add(dut):
    await test_op(dut, OPCODES["ADD"], 1, 2, op_ADD(1, 2))

@cocotb.test()
async def test_adc(dut):
    await test_op(dut, OPCODES["ADC"], 1, 2, op_ADC(1, 2))

@cocotb.test()
async def test_sub(dut):
    await test_op(dut, OPCODES["SUB"], 5, 1, op_SUB(5, 1))

@cocotb.test()
async def test_and(dut):
    await test_op(dut, OPCODES["AND"], 0xFFFF, 0x1234, op_AND(0xFFFF, 0x1234))

@cocotb.test()
async def test_or(dut):
    await test_op(dut, OPCODES["OR"], 0xF0F0, 0x0F0F, op_OR(0xF0F0, 0x0F0F))

@cocotb.test()
async def test_xor(dut):
    await test_op(dut, OPCODES["XOR"], 0b1010, 0b0110, op_XOR(0b1010, 0b0110))

@cocotb.test()
async def test_cmp(dut):
    await test_op(dut, OPCODES["CMP"], 666, 666, op_CMP(666, 666))
    await test_op(dut, OPCODES["CMP"], 1, 7, op_CMP(1, 7))

@cocotb.test()
async def test_inc(dut):
    await test_op(dut, OPCODES["INC"], 42, 0, op_INC(42))

@cocotb.test()
async def test_dec(dut):
    await test_op(dut, OPCODES["DEC"], 42, 0, op_DEC(42))

@cocotb.test()
async def test_shr(dut):
    await test_op(dut, OPCODES["SHR"], 8, 2, op_SHR(8, 2))

@cocotb.test()
async def test_shl(dut):
    await test_op(dut, OPCODES["SHL"], 8, 2, op_SHL(8, 2))
