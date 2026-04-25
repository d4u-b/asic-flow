# Python Function Map

This vault is an Obsidian-friendly map of the Python code in this project.

Use this note as the entry point when tracing behavior from CLI input down to flow execution.

## Start Here

- [[01_Execution_Path]]
- [[02_Module_cli]]
- [[03_Module_config]]
- [[04_Module_context]]
- [[05_Module_executor]]
- [[06_Module_registry]]
- [[07_Module_flows_base]]
- [[08_Module_flows_builtin]]
- [[09_Module_project_flows_custom_power]]

## Fast Trace

`python -m asic_flow`

1. Entry script: [src/asic_flow/__main__.py](../../src/asic_flow/__main__.py)
2. CLI entry: [[02_Module_cli#main]]
3. Manifest loading: [[03_Module_config#load_manifest]]
4. Executor creation: [[05_Module_executor#flowexecutor__init__]]
5. Flow listing or run dispatch: [[05_Module_executor#flowexecutorlist_flows]] or [[05_Module_executor#flowexecutorrun]]
6. Plugin loading: [[06_Module_registry#load_flow_class]]
7. Flow implementation: [[07_Module_flows_base]] and [[08_Module_flows_builtin]]
8. Custom plugin example: [[09_Module_project_flows_custom_power]]

## Python Files Covered

- [src/asic_flow/__main__.py](../../src/asic_flow/__main__.py)
- [src/asic_flow/cli.py](../../src/asic_flow/cli.py)
- [src/asic_flow/config.py](../../src/asic_flow/config.py)
- [src/asic_flow/context.py](../../src/asic_flow/context.py)
- [src/asic_flow/executor.py](../../src/asic_flow/executor.py)
- [src/asic_flow/registry.py](../../src/asic_flow/registry.py)
- [src/asic_flow/flows/base.py](../../src/asic_flow/flows/base.py)
- [src/asic_flow/flows/builtin.py](../../src/asic_flow/flows/builtin.py)
- [project_flows/custom_power.py](../../project_flows/custom_power.py)

## Notes

- This project is small and centered on a single runtime path: CLI -> manifest -> executor -> plugin loader -> flow class.
- Dataclasses like `FlowDefinition`, `Manifest`, and `FlowContext` are documented where they shape function behavior, even if they are not functions themselves.
