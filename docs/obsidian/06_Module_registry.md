# Module: `asic_flow.registry`

Back: [[00_Python_Function_Map]]

Source: [src/asic_flow/registry.py](../../src/asic_flow/registry.py)

## Purpose

This module resolves plugin strings like `asic_flow.flows.builtin:CommandFlow` into Python classes.

## Functions

### `add_plugin_paths`

- Source: [src/asic_flow/registry.py](../../src/asic_flow/registry.py#L11)
- Signature: `add_plugin_paths(paths: list[Path]) -> None`
- Role: inserts configured plugin directories into `sys.path`.
- Called by: [[05_Module_executor#flowexecutor__init__]]

### `load_flow_class`

- Source: [src/asic_flow/registry.py](../../src/asic_flow/registry.py#L18)
- Signature: `load_flow_class(target: str) -> Type[BaseFlow]`
- Role: imports a plugin module and returns the named class.
- Called by: [[05_Module_executor#flowexecutor_run_one]]
- Steps:
  - split target string by `:`
  - `importlib.import_module(module_name)`
  - `getattr(module, class_name, None)`
  - validate the result is a subclass of `BaseFlow`

## Trace Notes

- If a manifest plugin string is wrong, the failure will surface here.
- This is the bridge between configuration text and runtime Python classes.
