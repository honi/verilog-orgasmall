SIM ?= icarus
TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)
VERILOG_SOURCES = $(PWD)/../hdl/decoder.sv
TOPLEVEL := decoder
MODULE := test_decoder

include $(shell cocotb-config --makefiles)/Makefile.sim
