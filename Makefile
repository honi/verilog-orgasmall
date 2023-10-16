test_memory:
	./scripts/shell make -C src/memory/tests

test_registers:
	./scripts/shell make -C src/registers/tests

test_alu:
	./scripts/shell make -C src/alu/tests

.PHONY: clean test_memory test_registers test_alu
