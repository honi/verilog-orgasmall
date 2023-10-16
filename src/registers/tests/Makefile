SIM ?= icarus
TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)
VERILOG_SOURCES = $(PWD)/../hdl/registers.sv
TOPLEVEL := registers
MODULE := test_registers

include $(shell cocotb-config --makefiles)/Makefile.sim
