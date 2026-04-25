PYTHON ?= python3
PYTHONPATH_VALUE ?= src
MANIFEST ?= project.yaml
FLOW ?= ram_gate

.PHONY: help list list-details dry-run run ram-demo clean-demo

help:
	@printf '%s\n' \
		'Demo targets:' \
		'  make list                    List enabled flows' \
		'  make list-details            List flows with dependencies and plugins' \
		'  make dry-run FLOW=ram_gate   Print commands for a flow without executing' \
		'  make run FLOW=quality        Run a selected flow' \
		'  make ram-demo                Run the RAM integration demo flow chain' \
		'  make clean-demo              Remove generated demo outputs'

list:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) -m asic_flow --manifest $(MANIFEST) list

list-details:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) -m asic_flow --manifest $(MANIFEST) list --details

dry-run:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) -m asic_flow --manifest $(MANIFEST) run $(FLOW) --dry-run

run:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) -m asic_flow --manifest $(MANIFEST) run $(FLOW)

ram-demo:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) -m asic_flow --manifest $(MANIFEST) run ram_gate

clean-demo:
	rm -rf build/ram filelists reports/ram reports/ram_rtl.txt reports/ram_constraints.txt reports/ram_verify.txt reports/ram_gate.txt
