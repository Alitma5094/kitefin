CC = src/main.py
TEST_RUNNER = tests/test_compiler --verbose --keep-asm-on-failure
CHAPTER ?= 2

run:
	arch -x86_64 $(TEST_RUNNER) --chapter $(CHAPTER) --stage run $(CC)

.PHONY: %
lex:
	$(TEST_RUNNER) --chapter $(CHAPTER) --stage lex $(CC)

parse:
	$(TEST_RUNNER) --chapter $(CHAPTER) --stage parse $(CC)

codegen:
	$(TEST_RUNNER) --chapter $(CHAPTER) --stage codegen $(CC)

.PHONY: help
help:
	@echo "Usage: make [stage] [CHAPTER=n]"
	@echo "Example: make parse CHAPTER=5"
