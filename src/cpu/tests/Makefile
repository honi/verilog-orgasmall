SIM ?= icarus
TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)
VERILOG_SOURCES = $(PWD)/../hdl/cpu.sv
TOPLEVEL := cpu
MODULE := test_cpu

include $(shell cocotb-config --makefiles)/Makefile.sim
