# Module: `asic_flow.config`

Back: [[00_Python_Function_Map]]

Source: [src/asic_flow/config.py](../../src/asic_flow/config.py)

## Purpose

This module parses TOML or YAML manifests and normalizes them into runtime dataclasses.

## Key Data Structures

### `FlowDefinition`

- Source: [src/asic_flow/config.py](../../src/asic_flow/config.py#L9)
- Role: normalized per-flow configuration used at runtime.
- Consumed by: [[05_Module_executor]], [[07_Module_flows_base]], [[08_Module_flows_builtin]], [[09_Module_project_flows_custom_power]]

### `Manifest`

- Source: [src/asic_flow/config.py](../../src/asic_flow/config.py#L25)
- Role: top-level project runtime configuration, including all flows.
- Consumed by: [[05_Module_executor#flowexecutor__init__]]

## Functions

### `_read_toml`

- Source: [src/asic_flow/config.py](../../src/asic_flow/config.py#L37)
- Signature: `_read_toml(path: Path) -> dict[str, Any]`
- Role: reads a TOML manifest through the standard library `tomllib`.
- Called by: [[03_Module_config#_read_manifest]]

### `_read_yaml`

- Source: [src/asic_flow/config.py](../../src/asic_flow/config.py#L42)
- Signature: `_read_yaml(path: Path) -> dict[str, Any]`
- Role: reads a YAML manifest using `yaml.safe_load`.
- Called by: [[03_Module_config#_read_manifest]]
- Error path: raises a `RuntimeError` if `PyYAML` is not installed.

### `_read_manifest`

- Source: [src/asic_flow/config.py](../../src/asic_flow/config.py#L59)
- Signature: `_read_manifest(path: Path) -> dict[str, Any]`
- Role: chooses TOML or YAML reader by file extension.
- Called by: [[03_Module_config#load_manifest]]
- Calls:
  - [[03_Module_config#_read_toml]]
  - [[03_Module_config#_read_yaml]]

### `_as_list_of_str`

- Source: [src/asic_flow/config.py](../../src/asic_flow/config.py#L68)
- Signature: `_as_list_of_str(name: str, values: Any) -> list[str]`
- Role: validates and normalizes manifest fields like `depends_on`, `inputs`, `outputs`, and `tags`.
- Called by: [[03_Module_config#load_manifest]]

### `_as_commands`

- Source: [src/asic_flow/config.py](../../src/asic_flow/config.py#L76)
- Signature: `_as_commands(values: Any) -> list[list[str]]`
- Role: validates shell command definitions in a flow.
- Called by: [[03_Module_config#load_manifest]]

### `load_manifest`

- Source: [src/asic_flow/config.py](../../src/asic_flow/config.py#L89)
- Signature: `load_manifest(path: str | Path) -> Manifest`
- Role: converts raw manifest content into a validated `Manifest` object.
- Called by: [[02_Module_cli#_load_executor]]
- Calls:
  - [[03_Module_config#_read_manifest]]
  - [[03_Module_config#_as_list_of_str]]
  - [[03_Module_config#_as_commands]]
- Produces:
  - `project_root`, `workspace_root`, `logs_root`
  - `plugin_paths`
  - one `FlowDefinition` per `[[flow]]` or YAML `flow:` entry

## Trace Notes

- If a run fails before any flow starts, this module is a likely source.
- Most schema validation errors originate here.
