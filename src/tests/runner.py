from pathlib import Path
from cocotb.runner import get_runner


def test_module(name):
    basedir = Path(__file__).resolve().parent.parent.parent
    srcdir = basedir / "src" / "hdl"
    runner = get_runner("icarus")
    runner.build(
        always=True,
        hdl_toplevel=name,
        verilog_sources=[srcdir / f"{name}.sv"],
        build_dir=basedir / "build" / name,
        build_args=["-I", f"{srcdir}"],
        timescale=["1us", "1us"],
        defines={f"SIM_{name.upper()}": True}
    )
    runner.test(hdl_toplevel=name, test_module=f"test_{name}")
