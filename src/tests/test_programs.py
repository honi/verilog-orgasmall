import cocotb
from runner import test_module, run_program
from assembler import assemble_program


@cocotb.test()
async def test_loop1(dut):
    program = assemble_program("loop1.asm")
    await run_program(dut, program, 8)
    assert dut.registers.data[0].value == 0x21
    assert dut.pc.value == 5


@cocotb.test()
async def test_array_sum(dut):
    program = assemble_program("array_sum.asm")
    await run_program(dut, program, 36)
    assert dut.registers.data[3].value == 1 + 2 + 3 + 4


if __name__ == "__main__":
    test_module("cpu", "programs")
