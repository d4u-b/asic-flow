from __future__ import annotations

import os
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from asic_flow.config import FlowDefinition
from asic_flow.context import FlowContext


class BaseFlow(ABC):
    def __init__(self, definition: FlowDefinition, context: FlowContext) -> None:
        self.definition = definition
        self.context = context

    @property
    def name(self) -> str:
        return self.definition.name

    @property
    def workdir(self) -> Path:
        return self.context.resolve_path(self.definition.workdir)

    def build_env(self) -> dict[str, str]:
        env = dict(os.environ)
        env.update(self.context.env)
        env.update(self.context.project_env)
        env.update(self.definition.env)
        env["ASIC_FLOW_NAME"] = self.definition.name
        env["ASIC_PROJECT_NAME"] = self.context.project_name
        env["ASIC_PROJECT_ROOT"] = str(self.context.project_root)
        env["ASIC_WORKSPACE_ROOT"] = str(self.context.workspace_root)
        env["ASIC_LOGS_ROOT"] = str(self.context.logs_root)
        return env

    def run_command(self, command: list[str]) -> None:
        printable = " ".join(command)
        print(f"[{self.name}] {printable}")
        if self.context.dry_run:
            return
        subprocess.run(command, cwd=self.workdir, env=self.build_env(), check=True)

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError
