# Module: `asic_flow.context`

Back: [[00_Python_Function_Map]]

Source: [src/asic_flow/context.py](../../src/asic_flow/context.py)

## Purpose

This module holds runtime context shared across flows.

## Key Data Structure

### flowcontext

- Source: [src/asic_flow/context.py](../../src/asic_flow/context.py#L8)
- Symbol: `FlowContext`
- Created by: [[05_Module_executor#flowexecutor__init__]]
- Consumed by: [[07_Module_flows_base]]
- Fields:
  - project identity and manifest path
  - workspace and logs roots
  - project-wide environment
  - `dry_run`
  - mutable `state`

## Methods

### flowcontextresolve_path

- Source: [src/asic_flow/context.py](../../src/asic_flow/context.py#L20)
- Symbol: `FlowContext.resolve_path`
- Signature: `resolve_path(self, value: str | None) -> Path`
- Role: converts a manifest workdir value into an absolute path.
- Called by: [[07_Module_flows_base#baseflowworkdir]]
- Behavior:
  - empty value -> `project_root`
  - absolute value -> unchanged
  - relative value -> resolved against `project_root`
