# ASIC Flow Controller

This is a small Python framework for managing ASIC project flows from one entry point.

It is built around three ideas:

- One manifest file describes the project and the enabled flows.
- Each flow can depend on earlier flows such as `rtl -> simulation/synthesis -> quality`.
- New flows can be added either as simple command entries in the manifest or as custom Python plugins.

## Structure

```text
asic_flow/
├── project.toml              # Example TOML manifest
├── project.yaml              # Example YAML manifest
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
PYTHONPATH=src python3 -m asic_flow --manifest project.yaml list
PYTHONPATH=src python3 -m asic_flow --manifest project.yaml run quality
PYTHONPATH=src python3 -m asic_flow run --all --dry-run
```

For the included demo, a small `Makefile` is also provided:

```bash
make list
make list-details
make dry-run FLOW=ram_gate
make ram-demo
```

You can also install it as a local CLI:

```bash
python3 -m pip install -e .
asic-flow list
asic-flow run quality
```

## Manifest Model

The runner supports both `TOML` and `YAML` manifests.

- `project.toml`
- `project.yaml`
- `project.yml`

`TOML` remains the simpler default. `YAML` support requires `PyYAML`.

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

Equivalent YAML:

```yaml
project:
  name: demo_asic

runtime:
  workspace_root: work
  logs_root: logs
  plugin_paths:
    - project_flows

flow:
  - name: rtl
    plugin: asic_flow.flows.builtin:RTLFlow
    commands:
      - ["bash", "-lc", "make rtl"]

  - name: simulation
    depends_on:
      - rtl
    plugin: asic_flow.flows.builtin:SimulationFlow
    commands:
      - ["bash", "-lc", "make sim"]
```

You can also split large manifests with `include`. Include paths are resolved
relative to the manifest that declares them. Included manifests are loaded
first, and their `flow` entries are appended in include order.

```yaml
project:
  name: demo_asic

runtime:
  plugin_paths:
    - project_flows

include:
  - flows/core.yaml
  - flows/ram.yaml
```

Example included file:

```yaml
# flows/ram.yaml
flow:
  - name: ram_prep
    plugin: ram_integration:RamPrepFlow

  - name: ram_verify
    depends_on:
      - ram_prep
    plugin: asic_flow.flows.builtin:SimulationFlow
    commands:
      - ["bash", "-lc", "make sim_ram"]
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

Then register it in your manifest:

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

## RAM Integration Demo

The repository includes a demo RAM-integration sequence that matches a common SoC workflow:

- update RAM-generation inputs
- remove stale generated RAM outputs
- rebuild `.f` filelists for generated RTL and Liberty
- review RTL, wiring, and CSR changes
- update synthesis constraints
- run simulation
- pass a final gate before a manual commit

The demo plugin lives in `project_flows/ram_integration.py` and exposes:

- `RamPrepFlow`
- `RamCollateralFlow`

Example run:

```bash
PYTHONPATH=src python3 -m asic_flow run ram_gate
```

That run executes:

```text
ram_prep -> ram_collateral -> ram_rtl -> ram_constraints -> ram_verify -> ram_gate
```

The Python plugin creates placeholder collateral under:

- `build/ram/`
- `filelists/`
- `reports/ram/`

Replace the placeholder logic with your actual RAM compiler command, cleanup rules, and filelist generation once you wire it into your SoC project.

The example `project.yaml` now stays short by including:

- `flows/core.yaml`
- `flows/ram.yaml`

## Why this scales

- You keep orchestration logic in one place.
- You can grow from simple shell wrappers to richer Python plugins without changing the runner.
- Dependencies are explicit, so larger projects stay manageable.
- TOML uses the standard library, and YAML is available through `PyYAML`.
