MODULES := $(patsubst src/%,%,$(shell find src -type d -depth 1))

all: $(MODULES)

$(MODULES):
	./scripts/shell make -C src/$@/tests

clean:
	find src -name "*.vcd" -o -name "results.xml" -o -name "sim_build" -o -name "__pycache__" | xargs rm -r

.PHONY: all clean $(MODULES)
