# MODULES := $(patsubst src/%,%,$(shell find src -type d -maxdepth 1))
MODULES := memory cpu decoder registers alu

all: $(MODULES)

$(MODULES):
	./scripts/shell make -C src/$@/tests

synth/%.json: src/*/hdl/%.sv
	-mkdir synth
	./scripts/shell yosys -p "prep -top $(basename $(notdir $@)); write_json $@" $<

synth/%.svg: synth/%.json
	./scripts/shell netlistsvg $< -o $@

clean:
	find src -name "*.vcd" -o -name "results.xml" -o -name "sim_build" -o -name "__pycache__" | xargs rm -r

.PHONY: all clean $(MODULES)
