default:
	@echo "--->Please specify one of the following:"
	@echo "--->[refresh] [rebuild] [clean] [tree] [run]"

SHELL:=/usr/bin/env bash

refresh: clean tree

rebuild: clean tree run

clean:
	make -f make/clean.mk 
tree:
	make -f make/tree.mk 
run:
	make -f make/run.mk



