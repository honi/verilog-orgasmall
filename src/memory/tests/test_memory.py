import random

import cocotb
from cocotb.triggers import FallingEdge
from cocotb.clock import Clock


@cocotb.test()
async def memory_basic_test(dut):
    clock = Clock(dut.clk, 10, "us")
    cocotb.start_soon(clock.start(start_high=False))

    dut.rst.value = 1
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 0

    dut.we.value = 1
    dut.oe.value = 0
    dut.addr.value = 0x1000
    dut.data_in.value = 0xAAAA
    await FallingEdge(dut.clk)

    dut.we.value = 1
    dut.oe.value = 0
    dut.addr.value = 0x2000
    dut.data_in.value = 0xFFFF
    await FallingEdge(dut.clk)

    dut.we.value = 0
    dut.oe.value = 1
    dut.addr.value = 0x1000
    await FallingEdge(dut.clk)
    assert dut.data_out.value == 0xAAAA, f"{dut.data_out.value} != 0xAAAA"

    dut.we.value = 0
    dut.oe.value = 1
    dut.addr.value = 0x2000
    await FallingEdge(dut.clk)
    assert dut.data_out.value == 0xFFFF, f"{dut.data_out.value} != 0xFFFF"


@cocotb.test()
async def memory_randomised_test(dut):
    clock = Clock(dut.clk, 10, "us")
    cocotb.start_soon(clock.start(start_high=False))

    dut.rst.value = 1
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 0

    for _ in range(10):
        addr = random.randint(0, 2**16)
        data = random.randint(0, 2**16)

        dut.we.value = 1
        dut.oe.value = 0
        dut.addr.value = addr
        dut.data_in.value = data
        await FallingEdge(dut.clk)

        dut.we.value = 0
        dut.oe.value = 1
        dut.addr.value = addr
        await FallingEdge(dut.clk)
        assert dut.data_out.value == data, f"{dut.data_out.value} != {data}"
