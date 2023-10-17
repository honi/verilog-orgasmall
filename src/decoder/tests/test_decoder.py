import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def test_type_a(dut):
    opcode = 13
    rx = 2
    ry = 3
    dut.inst_hi.value = (opcode << 3) | rx
    dut.inst_lo.value = ry << 5
    await Timer(1, "us")
    assert dut.opcode.value == opcode
    assert dut.rx.value == rx
    assert dut.ry.value == ry


@cocotb.test()
async def test_type_b(dut):
    opcode = 6
    rx = 7
    dut.inst_hi.value = (opcode << 3) | rx
    dut.inst_lo.value = 0
    await Timer(1, "us")
    assert dut.opcode.value == opcode
    assert dut.rx.value == rx


@cocotb.test()
async def test_type_c(dut):
    opcode = 1
    imm = 255
    dut.inst_hi.value = opcode << 3
    dut.inst_lo.value = imm
    await Timer(1, "us")
    assert dut.opcode.value == opcode
    assert dut.imm.value == imm


@cocotb.test()
async def test_type_d(dut):
    opcode = 0b11111
    rx = 0
    imm = 0xAA
    dut.inst_hi.value = (opcode << 3) | rx
    dut.inst_lo.value = imm
    await Timer(1, "us")
    assert dut.opcode.value == opcode
    assert dut.rx.value == rx
    assert dut.imm.value == imm
