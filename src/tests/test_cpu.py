import cocotb
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.clock import Clock
from cocotb.types import LogicArray, Range

from config import *
from isa import *
from runner import test_module


async def run_program(dut, program):
    # Cargamos el programa en memoria.
    for addr in range (1 << ADDR_SIZE):
        dut.inst_memory.data[addr].value = program[addr] if addr < len(program) else 0

    # Configuramos el clock y nos sincronizamos.
    clock = Clock(dut.clk, 10, "us")
    cocotb.start_soon(clock.start(start_high=False))

    # Reset cycle.
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # Single-cycle for the win!
    # Necesitamos len(program) ciclos para ejecutar todo el programa.
    # TODO: Sumamos 1 ciclo más en caso de que la última instrucción sea un store a memoria?
    await ClockCycles(dut.clk, len(program))


async def test_op(dut, opcode, *operands):
    await run_program(dut, [
        encode(SET, rx=1, imm=operands[0] if len(operands) >= 1 else 0),
        encode(SET, rx=2, imm=operands[1] if len(operands) >= 2 else 0),
        encode(opcode, rx=1, ry=2),
    ])
    expected = OPFUNCS[opcode](*operands)
    assert LogicArray(dut.registers.data[1].value) == LogicArray(expected, Range(WORD_SIZE-1, 'downto', 0))


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

@cocotb.test()
async def test_load_store_imm(dut):
    addr = 0x0F
    data = 42
    await run_program(dut, [
        encode(SET, rx=1, imm=data),
        encode(STR, rx=1, imm=addr),
        encode(LOAD, rx=2, imm=addr),
    ])
    assert dut.data_memory.data[addr].value == data
    assert dut.registers.data[2].value == data

@cocotb.test()
async def test_load_store_reg(dut):
    addr = 0x0F
    data = 42
    await run_program(dut, [
        encode(SET, rx=1, imm=data),
        encode(SET, rx=2, imm=addr),
        encode(RSTR, rx=2, ry=1),
        encode(RLOAD, rx=3, ry=2),
    ])
    assert dut.data_memory.data[addr].value == data
    assert dut.registers.data[3].value == data

@cocotb.test()
async def test_jmp(dut):
    await run_program(dut, [
        encode(INC, rx=1),
        encode(JMP, imm=6),
        encode(INC, rx=1),
        encode(INC, rx=1),
        encode(INC, rx=1),
        encode(INC, rx=1),
        encode(INC, rx=1),
    ])
    assert dut.registers.data[1].value == 2

@cocotb.test()
async def test_jc(dut):
    await run_program(dut, [
        encode(SET, rx=1, imm=0xFF),
        encode(SET, rx=2, imm=1),
        encode(ADD, rx=1, ry=2),
        encode(JC, imm=6),
        encode(SET, rx=3, imm=1),
        encode(JMP, imm=0),
        encode(SET, rx=3, imm=42),
    ])
    assert dut.registers.data[3].value == 42

@cocotb.test()
async def test_jz(dut):
    await run_program(dut, [
        encode(SET, rx=1, imm=32),
        encode(SET, rx=2, imm=32),
        encode(SUB, rx=1, ry=2),
        encode(JZ, imm=6),
        encode(SET, rx=3, imm=1),
        encode(JMP, imm=0),
        encode(SET, rx=3, imm=42),
    ])
    assert dut.registers.data[3].value == 42

@cocotb.test()
async def test_jn(dut):
    await run_program(dut, [
        encode(SET, rx=1, imm=8),
        encode(SET, rx=2, imm=32),
        encode(SUB, rx=1, ry=2),
        encode(JN, imm=6),
        encode(SET, rx=3, imm=1),
        encode(JMP, imm=0),
        encode(SET, rx=3, imm=42),
    ])
    assert dut.registers.data[3].value == 42


if __name__ == "__main__":
    test_module("cpu")
