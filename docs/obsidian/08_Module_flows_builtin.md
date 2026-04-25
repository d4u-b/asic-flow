# Module: `asic_flow.flows.builtin`

Back: [[00_Python_Function_Map]]

Source: [src/asic_flow/flows/builtin.py](../../src/asic_flow/flows/builtin.py)

## Purpose

This module provides stock flow classes that mainly wrap manifest-defined shell commands.

## Classes

### commandflow

- Source: [src/asic_flow/flows/builtin.py](../../src/asic_flow/flows/builtin.py#L6)
- Symbol: `CommandFlow`
- Inherits: [[07_Module_flows_base#baseflow]]
- Role: generic flow implementation for `definition.commands`.

### commandflowrun

- Source: [src/asic_flow/flows/builtin.py](../../src/asic_flow/flows/builtin.py#L7)
- Symbol: `CommandFlow.run`
- Signature: `run(self) -> None`
- Role: validates that commands exist, then executes each command through `run_command`.
- Calls: [[07_Module_flows_base#baseflowrun_command]]

### rtlflow

- Source: [src/asic_flow/flows/builtin.py](../../src/asic_flow/flows/builtin.py#L14)
- Symbol: `RTLFlow`
- Inherits: `CommandFlow`
- Role: semantic alias for RTL preparation or lint flows.

### simulationflow

- Source: [src/asic_flow/flows/builtin.py](../../src/asic_flow/flows/builtin.py#L18)
- Symbol: `SimulationFlow`
- Inherits: `CommandFlow`
- Role: semantic alias for simulation flows.

### synthesisflow

- Source: [src/asic_flow/flows/builtin.py](../../src/asic_flow/flows/builtin.py#L22)
- Symbol: `SynthesisFlow`
- Inherits: `CommandFlow`
- Role: semantic alias for synthesis flows.

### qualitycheckflow

- Source: [src/asic_flow/flows/builtin.py](../../src/asic_flow/flows/builtin.py#L26)
- Symbol: `QualityCheckFlow`
- Inherits: `CommandFlow`
- Role: semantic alias for quality or signoff checks.

## Trace Notes

- These subclasses do not override `run()`, so behavior still flows through [[08_Module_flows_builtin#commandflowrun]].
- When the manifest uses builtin plugin strings, most runtime behavior is inherited rather than locally implemented.
