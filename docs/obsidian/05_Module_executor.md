# Module: `asic_flow.executor`

Back: [[00_Python_Function_Map]]

Source: [src/asic_flow/executor.py](../../src/asic_flow/executor.py)

## Purpose

This module coordinates flow execution, dependency traversal, plugin loading, and runtime context construction.

## Class

### flowexecutor

- Source: [src/asic_flow/executor.py](../../src/asic_flow/executor.py#L10)
- Symbol: `FlowExecutor`
- Role: central runtime orchestrator.

## Methods

### flowexecutor__init__

- Source: [src/asic_flow/executor.py](../../src/asic_flow/executor.py#L11)
- Symbol: `FlowExecutor.__init__`
- Signature: `__init__(self, manifest: Manifest, dry_run: bool = False) -> None`
- Role: stores the manifest, builds a `FlowContext`, and registers extra plugin search paths.
- Called by: [[02_Module_cli#_load_executor]]
- Calls:
  - `FlowContext(...)`
  - [[06_Module_registry#add_plugin_paths]]

### flowexecutorlist_flows

- Source: [src/asic_flow/executor.py](../../src/asic_flow/executor.py#L25)
- Symbol: `FlowExecutor.list_flows`
- Signature: `list_flows(self) -> list[FlowDefinition]`
- Role: returns enabled flows only.
- Called by: [[02_Module_cli#main]]

### flowexecutorrun

- Source: [src/asic_flow/executor.py](../../src/asic_flow/executor.py#L28)
- Symbol: `FlowExecutor.run`
- Signature: `run(self, targets: Iterable[str]) -> None`
- Role: prepares runtime directories and starts recursive execution for each target flow.
- Called by: [[02_Module_cli#main]]
- Calls: [[05_Module_executor#flowexecutor_run_one]]

### flowexecutor_run_one

- Source: [src/asic_flow/executor.py](../../src/asic_flow/executor.py#L36)
- Symbol: `FlowExecutor._run_one`
- Signature: `_run_one(self, name: str, visited: set[str], active: set[str]) -> None`
- Role: depth-first execution of one flow with cycle detection.
- Called by: [[05_Module_executor#flowexecutorrun]] and recursively by itself
- Calls:
  - itself for each dependency
  - [[06_Module_registry#load_flow_class]]
  - `flow_class(definition, self.context)`
  - `flow.run()`
- Important checks:
  - already visited -> skip
  - active recursion stack -> dependency cycle error
  - missing flow -> unknown flow error
  - disabled flow -> disabled flow error

## Trace Notes

- If you need the exact point where dependency ordering happens, this is the note to start from.
- All plugin instances are created here, not in the CLI layer.
