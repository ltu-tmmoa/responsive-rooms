default: help

test:
	@cd test/ && $(MAKE) --no-print-directory

help:
	@echo "> Available Commands:"
	@echo "make test     - Runs integration test suite."
	@echo "make help     - Displays this help message."

.PHONY: default test help
