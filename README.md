# ASIC Flow Controller

This is a small Python framework for managing ASIC project flows from one entry point.

It is built around three ideas:

- One manifest file describes the project and the enabled flows.
- Each flow can depend on earlier flows such as `rtl -> simulation/synthesis -> quality`.
- New flows can be added either as simple command entries in the manifest or as custom Python plugins.

## Structure

```text
asic_flow/
├── project.toml              # Example manifest
├── project_flows/            # Local custom Python flow plugins
└── src/asic_flow/
    ├── cli.py                # CLI entry point
    ├── config.py             # Manifest loader
    ├── executor.py           # Dependency-aware runner
    ├── registry.py           # Plugin loader
    └── flows/
        ├── base.py           # Base flow API
        └── builtin.py        # Built-in command flows
```

## Run

From this directory:

```bash
PYTHONPATH=src python3 -m asic_flow list
```

Typical usage:

```bash
PYTHONPATH=src python3 -m asic_flow list
PYTHONPATH=src python3 -m asic_flow run quality
PYTHONPATH=src python3 -m asic_flow run --all --dry-run
```

You can also install it as a local CLI:

```bash
python3 -m pip install -e .
asic-flow list
asic-flow run quality
```

## Manifest Model

The manifest is `project.toml`.

```toml
[project]
name = "demo_asic"

[runtime]
workspace_root = "work"
logs_root = "logs"
plugin_paths = ["project_flows"]

[[flow]]
name = "rtl"
plugin = "asic_flow.flows.builtin:RTLFlow"
commands = [
  ["bash", "-lc", "make rtl"],
]

[[flow]]
name = "simulation"
depends_on = ["rtl"]
plugin = "asic_flow.flows.builtin:SimulationFlow"
commands = [
  ["bash", "-lc", "make sim"],
]
```

## Add A New Flow

### Option 1: command-only flow

This is the fastest path when the flow is just a shell command:

```toml
[[flow]]
name = "lint"
depends_on = ["rtl"]
plugin = "asic_flow.flows.builtin:CommandFlow"
commands = [
  ["bash", "-lc", "make lint"],
]
```

### Option 2: custom Python plugin

Use this when the flow needs dynamic logic, parsing, conditional reruns, or tool-specific setup.

Create a file under `project_flows/`, for example `project_flows/formal.py`:

```python
from asic_flow.flows.base import BaseFlow

class FormalFlow(BaseFlow):
    def run(self) -> None:
        self.run_command(["bash", "-lc", "make formal"])
```

Then register it in `project.toml`:

```toml
[[flow]]
name = "formal"
plugin = "formal:FormalFlow"
depends_on = ["rtl"]
```

Because `project_flows` is already listed in `runtime.plugin_paths`, no extra packaging is needed.

If the plugin needs custom settings, add them under `options`:

```toml
[[flow]]
name = "power"
plugin = "custom_power:PowerFlow"
depends_on = ["synthesis"]
options = { mode = "saif" }
```

## Why this scales

- You keep orchestration logic in one place.
- You can grow from simple shell wrappers to richer Python plugins without changing the runner.
- Dependencies are explicit, so larger projects stay manageable.
- The implementation uses only the Python standard library.
