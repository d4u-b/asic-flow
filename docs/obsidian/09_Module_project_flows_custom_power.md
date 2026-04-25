# Module: `project_flows.custom_power`

Back: [[00_Python_Function_Map]]

Source: [project_flows/custom_power.py](../../project_flows/custom_power.py)

## Purpose

This is the example custom plugin shipped with the project.

## Class

### powerflow

- Source: [project_flows/custom_power.py](../../project_flows/custom_power.py#L6)
- Symbol: `PowerFlow`
- Inherits: [[07_Module_flows_base#baseflow]]
- Role: demonstrates how a custom plugin can read `definition.options` and construct a command dynamically.

### powerflowrun

- Source: [project_flows/custom_power.py](../../project_flows/custom_power.py#L7)
- Symbol: `PowerFlow.run`
- Signature: `run(self) -> None`
- Role: reads `options["mode"]`, builds a `bash -lc` command, and delegates execution to `run_command`.
- Calls: [[07_Module_flows_base#baseflowrun_command]]

## Trace Notes

- This note is useful when tracing plugin behavior outside the builtins package.
- Manifest string example: `custom_power:PowerFlow`
