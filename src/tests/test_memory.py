import random
import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
from cocotb.types import LogicArray

from config import *
from runner import test_module


X = LogicArray("X" * WORD_SIZE)
Z = LogicArray("Z" * WORD_SIZE)


@cocotb.test()
async def memory_basic_test(dut):
    # Estado inicial.
    dut.data_in.value = 0
    dut.addr.value = 0
    dut.en_write.value = 0
    dut.rst.value = 0

    # Configuramos el clock y nos sincronizamos.
    clock = Clock(dut.clk, 10, "us")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)

    # TODO: No se si vale la pena chequear esto.
    assert LogicArray(dut.data_out.value) == X

    # Reset cycle.
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # Testeamos escribir y leer varios datos al azar.
    for _ in range(10):
        data = random.randint(0, 2**WORD_SIZE)
        addr = random.randint(0, 2**ADDR_SIZE)

        dut.data_in.value = data
        dut.addr.value = addr
        dut.en_write.value = 1

        # TODO: Revisar alternativa para el doble RisingEdge.
        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)

        assert dut.data_out.value == data


if __name__ == "__main__":
    test_module("memory")
