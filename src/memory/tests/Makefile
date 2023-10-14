SIM ?= icarus
TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)
VERILOG_SOURCES = $(PWD)/../hdl/memory.sv
TOPLEVEL := memory
MODULE := test_memory

include $(shell cocotb-config --makefiles)/Makefile.sim
