from __future__ import annotations

from asic_flow.flows.base import BaseFlow


class CommandFlow(BaseFlow):
    """Run each configured command in order for a manifest-defined flow."""

    def run(self) -> None:
        if not self.definition.commands:
            raise ValueError(f"flow {self.name} does not define any commands")
        for command in self.definition.commands:
            self.run_command(command)


class RTLFlow(CommandFlow):
    """RTL preparation or lint-style flow."""


class SimulationFlow(CommandFlow):
    """Simulation flow."""


class SynthesisFlow(CommandFlow):
    """Synthesis flow."""


class QualityCheckFlow(CommandFlow):
    """Quality and signoff checks."""
