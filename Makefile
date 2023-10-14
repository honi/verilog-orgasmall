test_memory:
	./scripts/shell make -C src/memory/tests

test_alu:
	./scripts/shell make -C src/alu/tests

.PHONY: test_memory test_alu
