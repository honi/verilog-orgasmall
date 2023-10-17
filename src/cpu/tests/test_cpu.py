import random
import cocotb
from cocotb.triggers import RisingEdge, Timer, ClockCycles
from cocotb.clock import Clock
from cocotb.types import LogicArray, Range


def assign_memory(target, data):
    for i, d in enumerate(data):
        target[i].value = d

def encode_inc(rx):
    return ((0b11000 << 3) | rx) << 8


@cocotb.test()
async def cpu_basic_test(dut):
    # Asignamos en la memoria de instrucciones un programita de prueba.
    program = [
        encode_inc(1),
        encode_inc(1),
        encode_inc(2),
        encode_inc(2),
        encode_inc(1),
        encode_inc(1),
        encode_inc(1),
    ]
    assign_memory(dut.inst_memory.data, program)

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

    # Revisamos los valores de los registros.
    assert dut.registers.data[1] == 5
    assert dut.registers.data[2] == 2
