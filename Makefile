MODULES := $(patsubst src/tests/test_%.py,%,$(shell find src/tests -name "test_*.py"))

all: $(MODULES)

$(MODULES):
	./scripts/shell python3 src/tests/test_$@.py

synth/%.json: src/*/hdl/%.sv
	-mkdir synth
	./scripts/shell yosys -p "prep -top $(basename $(notdir $@)); write_json $@" $<

synth/%.svg: synth/%.json
	./scripts/shell netlistsvg $< -o $@

clean:
	rm -r build

.PHONY: all clean $(MODULES)
