TESTABLES = actuator-master master-actuator master-sensor master-terminal \
            terminal-master

default:
	@echo "Running integration tests ..."
	@$(foreach TESTABLE,$(TESTABLES), \
		@echo ">> $(TESTABLE)" $(\n) \
		@cd $(TESTABLE) && $(MAKE) start-test --no-print-directory $(\n) \
		@cd $(TESTABLE) && $(MAKE) start-tested-process --no-print-directory $(\n) \
		@echo "" $(\n) \
	)

.PHONY: default

define \n


endef
