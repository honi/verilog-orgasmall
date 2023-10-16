import random
import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from cocotb.types import LogicArray, Range


# TODO: Compartir estos defaults con la definición de los parámetros en Verilog.
WORD_SIZE = 16
ADDR_SIZE = 16
X = LogicArray("X" * WORD_SIZE)
Z = LogicArray("Z" * WORD_SIZE)


@cocotb.test()
async def memory_basic_test(dut):
    # Estado inicial.
    dut.data_in.value = 0
    dut.addr.value = 0
    dut.we.value = 0
    dut.oe.value = 0
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
    expected_value = Z
    for _ in range(10):
        data = random.randint(0, 2**WORD_SIZE)
        addr = random.randint(0, 2**ADDR_SIZE)

        dut.we.value = 1
        dut.oe.value = 0
        dut.data_in.value = data
        dut.addr.value = addr
        await RisingEdge(dut.clk)

        # TODO: Revisar si está bien hacer el assert acá.
        assert LogicArray(dut.data_out.value) == expected_value
        expected_value = LogicArray(data, Range(WORD_SIZE-1, 'downto', 0))

        dut.we.value = 0
        dut.oe.value = 1
        dut.addr.value = addr
        await RisingEdge(dut.clk)
