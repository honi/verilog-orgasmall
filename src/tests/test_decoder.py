import cocotb
from cocotb.triggers import Timer

from isa import *
from runner import test_module


@cocotb.test()
async def test_type_a(dut):
    dut.inst.value = encode(ADD, rx=1, ry=2)
    await Timer(1, "us")
    assert dut.opcode.value == ADD
    assert dut.rx.value == 1
    assert dut.ry.value == 2


@cocotb.test()
async def test_type_b(dut):
    dut.inst.value = encode(INC, rx=1)
    await Timer(1, "us")
    assert dut.opcode.value == INC
    assert dut.rx.value == 1


@cocotb.test()
async def test_type_c(dut):
    dut.inst.value = encode(JMP, imm=0xAA)
    await Timer(1, "us")
    assert dut.opcode.value == JMP
    assert dut.imm.value == 0xAA


@cocotb.test()
async def test_type_d(dut):
    dut.inst.value = encode(SET, rx=1, imm=0xAA)
    await Timer(1, "us")
    assert dut.opcode.value == SET
    assert dut.rx.value == 1
    assert dut.imm.value == 0xAA


if __name__ == "__main__":
    test_module("decoder")
