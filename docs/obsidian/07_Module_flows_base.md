# Module: `asic_flow.flows.base`

Back: [[00_Python_Function_Map]]

Source: [src/asic_flow/flows/base.py](../../src/asic_flow/flows/base.py)

## Purpose

This module defines the shared base API for all flows.

## Class

### baseflow

- Source: [src/asic_flow/flows/base.py](../../src/asic_flow/flows/base.py#L12)
- Symbol: `BaseFlow`
- Role: shared logic for naming, workdir resolution, environment construction, and command execution.
- Subclasses:
  - [[08_Module_flows_builtin#commandflow]]
  - [[08_Module_flows_builtin#rtlflow]]
  - [[08_Module_flows_builtin#simulationflow]]
  - [[08_Module_flows_builtin#synthesisflow]]
  - [[08_Module_flows_builtin#qualitycheckflow]]
  - [[09_Module_project_flows_custom_power#powerflow]]

## Methods

### baseflow__init__

- Source: [src/asic_flow/flows/base.py](../../src/asic_flow/flows/base.py#L13)
- Symbol: `BaseFlow.__init__`
- Signature: `__init__(self, definition: FlowDefinition, context: FlowContext) -> None`
- Role: stores flow definition and runtime context.
- Called by: [[05_Module_executor#flowexecutor_run_one]]

### baseflowname

- Source: [src/asic_flow/flows/base.py](../../src/asic_flow/flows/base.py#L18)
- Symbol: `BaseFlow.name`
- Signature: `name(self) -> str`
- Role: convenience property exposing `definition.name`.

### baseflowworkdir

- Source: [src/asic_flow/flows/base.py](../../src/asic_flow/flows/base.py#L22)
- Symbol: `BaseFlow.workdir`
- Signature: `workdir(self) -> Path`
- Role: resolves the effective working directory for a flow.
- Calls: [[04_Module_context#flowcontextresolve_path]]

### baseflowbuild_env

- Source: [src/asic_flow/flows/base.py](../../src/asic_flow/flows/base.py#L25)
- Symbol: `BaseFlow.build_env`
- Signature: `build_env(self) -> dict[str, str]`
- Role: merges OS env, manifest env, project env, and flow env into one execution environment.
- Called by: [[07_Module_flows_base#baseflowrun_command]]

### baseflowrun_command

- Source: [src/asic_flow/flows/base.py](../../src/asic_flow/flows/base.py#L37)
- Symbol: `BaseFlow.run_command`
- Signature: `run_command(self, command: list[str]) -> None`
- Role: prints a command, honors `dry_run`, and otherwise executes it with `subprocess.run`.
- Called by:
  - [[08_Module_flows_builtin#commandflowrun]]
  - [[09_Module_project_flows_custom_power#powerflowrun]]
- Calls:
  - [[07_Module_flows_base#baseflowworkdir]]
  - [[07_Module_flows_base#baseflowbuild_env]]

### baseflowrun

- Source: [src/asic_flow/flows/base.py](../../src/asic_flow/flows/base.py#L44)
- Symbol: `BaseFlow.run`
- Signature: `run(self) -> None`
- Role: abstract method that each concrete flow must implement.
