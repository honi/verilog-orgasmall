import math
import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
from cocotb.types import LogicArray

from config import *
from runner import test_module


DATA_X = LogicArray("X" * WORD_SIZE)
DATA_Z = LogicArray("Z" * WORD_SIZE)
IDX_Z = LogicArray("Z" * REGISTER_BITS)


@cocotb.test()
async def registers_basic_test(dut):
    # Estado inicial.
    dut.data_in.value = DATA_Z
    dut.idx_write.value = IDX_Z
    dut.en_write.value = 0
    dut.idx_out_a.value = IDX_Z
    dut.idx_out_b.value = IDX_Z
    dut.rst.value = 0

    # Configuramos el clock y nos sincronizamos.
    clock = Clock(dut.clk, 10, "us")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)

    # TODO: No se si vale la pena chequear esto.
    # TODO: Conviene que las salidas sean 0 por defecto?
    assert LogicArray(dut.data_out_a.value) == DATA_X
    assert LogicArray(dut.data_out_b.value) == DATA_X

    # Reset cycle.
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # Escribimos en todos los registros.
    for i in range(NUM_REGISTERS):
        dut.data_in.value = 100 + i
        dut.idx_write.value = i
        dut.en_write.value = 1
        await RisingEdge(dut.clk)

    # Desactivamos la escritura.
    dut.data_in.value = DATA_Z
    dut.idx_write.value = IDX_Z
    dut.en_write.value = 0
    await RisingEdge(dut.clk)

    # Leemos todos los registros de a 2.
    for i in range(0, NUM_REGISTERS, 2):
        dut.idx_out_a.value = i
        dut.idx_out_b.value = i + 1
        await RisingEdge(dut.clk)
        assert dut.data_out_a.value == 100 + i
        assert dut.data_out_b.value == 100 + i + 1


if __name__ == "__main__":
    test_module("registers")
