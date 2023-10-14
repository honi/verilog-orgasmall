import cocotb
from cocotb.triggers import Timer


ADD = 0
SUB = 1
LEFT_SHIFT = 2
RIGHT_SHIFT_ARITHMETIC = 3
RIGHT_SHIFT_LOGIC = 4
AND = 5
OR = 6
XOR = 7
EQUAL = 8

async def test_op(dut, opcode, a, b, expected):
    dut.a.value = a
    dut.b.value = b
    dut.op.value = opcode
    await Timer(10, "us")
    assert dut.out.value == expected, f"{int(dut.out.value)} != {expected}"

@cocotb.test()
async def test_add(dut):
    await test_op(dut, ADD, 1, 2, 3)

@cocotb.test()
async def test_sub(dut):
    await test_op(dut, SUB, 5, 1, 4)

@cocotb.test()
async def test_left_shift(dut):
    await test_op(dut, LEFT_SHIFT, 3, 2, 12)

@cocotb.test()
async def test_right_shift_arithmetic(dut):
    await test_op(dut, RIGHT_SHIFT_ARITHMETIC, -8, 2, -2)

@cocotb.test()
async def test_right_shift_logic(dut):
    await test_op(dut, RIGHT_SHIFT_LOGIC, -1, 1, 2**15 - 1)

@cocotb.test()
async def test_and(dut):
    await test_op(dut, AND, 0xFFFF, 0x1234, 0x1234)

@cocotb.test()
async def test_or(dut):
    await test_op(dut, OR, 0xF0F0, 0x0F0F, 0xFFFF)

@cocotb.test()
async def test_xor(dut):
    await test_op(dut, XOR, 0b1010, 0b0110, 0b1100)

@cocotb.test()
async def test_equal(dut):
    await test_op(dut, EQUAL, 666, 666, 1)
    await test_op(dut, EQUAL, 1, 7, 0)
