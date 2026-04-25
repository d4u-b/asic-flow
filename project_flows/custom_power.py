from __future__ import annotations

from asic_flow.flows.base import BaseFlow


class PowerFlow(BaseFlow):
    """Example project-local plugin that writes a simple power report."""

    def run(self) -> None:
        mode = self.definition.options.get("mode", "vectorless")
        command = [
            "bash",
            "-lc",
            (
                "mkdir -p \"$REPORT_DIR\" && "
                f"echo \"Power analysis ({mode}) for $TOP\" > \"$REPORT_DIR/power.txt\""
            ),
        ]
        self.run_command(command)
