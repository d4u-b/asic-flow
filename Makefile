PYTHON ?= python3
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python
ASIC_FLOW := $(VENV)/bin/asic-flow
MANIFEST ?= project.yaml
FLOW ?= ram_gate

.PHONY: help venv setup reinstall list list-details dry-run run ram-demo clean-demo

help:
	@printf '%s\n' \
		'Demo targets:' \
		'  make setup                   Create .venv and install the local CLI' \
		'  make reinstall               Reinstall the local CLI into .venv' \
		'  make list                    List enabled flows' \
		'  make list-details            List flows with dependencies and plugins' \
		'  make dry-run FLOW=ram_gate   Print commands for a flow without executing' \
		'  make run FLOW=quality        Run a selected flow' \
		'  make ram-demo                Run the RAM integration demo flow chain' \
		'  make clean-demo              Remove generated demo outputs'

venv:
	$(PYTHON) -m venv --system-site-packages $(VENV)

setup: $(ASIC_FLOW)

$(ASIC_FLOW): pyproject.toml
	test -x $(VENV_PYTHON) || $(MAKE) venv
	$(VENV_PYTHON) -m pip install --no-build-isolation -e .

reinstall:
	$(VENV_PYTHON) -m pip install --no-build-isolation -e .

list: $(ASIC_FLOW)
	$(ASIC_FLOW) --manifest $(MANIFEST) list

list-details: $(ASIC_FLOW)
	$(ASIC_FLOW) --manifest $(MANIFEST) list --details

dry-run: $(ASIC_FLOW)
	$(ASIC_FLOW) --manifest $(MANIFEST) run $(FLOW) --dry-run

run: $(ASIC_FLOW)
	$(ASIC_FLOW) --manifest $(MANIFEST) run $(FLOW)

ram-demo: $(ASIC_FLOW)
	$(ASIC_FLOW) --manifest $(MANIFEST) run ram_gate

clean-demo:
	rm -rf build/ram filelists reports/ram reports/ram_rtl.txt reports/ram_constraints.txt reports/ram_verify.txt reports/ram_gate.txt
