# Module: `asic_flow.cli`

Back: [[00_Python_Function_Map]]

Source: [src/asic_flow/cli.py](../../src/asic_flow/cli.py)

## Purpose

This module owns the command-line interface. It is the human-facing entry into the runtime.

## Functions

### `build_parser`

- Source: [src/asic_flow/cli.py](../../src/asic_flow/cli.py#L10)
- Signature: `build_parser() -> argparse.ArgumentParser`
- Role: defines the `list` and `run` subcommands and shared `--manifest` option.
- Called by: [[02_Module_cli#main]]
- Calls: `argparse.ArgumentParser(...)`, `add_argument(...)`, `add_subparsers(...)`

### `_load_executor`

- Source: [src/asic_flow/cli.py](../../src/asic_flow/cli.py#L30)
- Signature: `_load_executor(manifest_arg: str, dry_run: bool = False) -> FlowExecutor`
- Role: converts the manifest path string into a `Path`, loads the manifest, and constructs a `FlowExecutor`.
- Called by: [[02_Module_cli#main]]
- Calls: [[03_Module_config#load_manifest]], `FlowExecutor(...)`

### `main`

- Source: [src/asic_flow/cli.py](../../src/asic_flow/cli.py#L35)
- Signature: `main() -> int`
- Role: top-level CLI dispatcher.
- Called by: [src/asic_flow/__main__.py](../../src/asic_flow/__main__.py)
- Calls:
  - [[02_Module_cli#build_parser]]
  - `parser.parse_args()`
  - [[02_Module_cli#_load_executor]]
  - [[05_Module_executor#flowexecutorlist_flows]]
  - [[05_Module_executor#flowexecutorrun]]
- Branches:
  - `list`: prints enabled flow names, optionally with dependency and plugin details.
  - `run`: resolves targets from `args.flows` or `--all`, then executes them.

## Trace Notes

- This is the best starting note when the question is "what command causes this behavior?"
- `main()` does not execute shell commands directly. It delegates all real work into `FlowExecutor`.
