from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class FlowContext:
    project_name: str
    manifest_path: Path
    project_root: Path
    workspace_root: Path
    logs_root: Path
    env: dict[str, str]
    project_env: dict[str, str]
    dry_run: bool = False
    state: dict[str, Any] = field(default_factory=dict)

    def resolve_path(self, value: str | None) -> Path:
        if not value:
            return self.project_root
        candidate = Path(value).expanduser()
        if candidate.is_absolute():
            return candidate
        return (self.project_root / candidate).resolve()
