from pathlib import Path

import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.clock import Clock

from config import *


def test_module(module_name, test_name=None):
    if test_name is None:
        test_name = module_name
    basedir = Path(__file__).resolve().parent.parent.parent
    srcdir = basedir / "src" / "hdl"
    runner = get_runner("icarus")
    runner.build(
        always=True,
        hdl_toplevel=module_name,
        verilog_sources=[srcdir / f"{module_name}.sv"],
        build_dir=basedir / "build" / module_name,
        build_args=["-I", f"{srcdir}"],
        timescale=["1us", "1us"],
        defines={f"SIM_{module_name.upper()}": True}
    )
    runner.test(hdl_toplevel=module_name, test_module=f"test_{test_name}")


async def run_program(dut, program, cycles=None):
    # Cargamos el programa en memoria.
    for addr in range (1 << ADDR_SIZE):
        value = program[addr] if addr < len(program) else 0
        dut.inst_memory.data[addr].value = value

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
    await ClockCycles(dut.clk, len(program) if cycles is None else cycles)
