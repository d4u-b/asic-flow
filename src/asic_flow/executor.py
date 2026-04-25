from __future__ import annotations

from collections.abc import Iterable

from asic_flow.config import FlowDefinition, Manifest
from asic_flow.context import FlowContext
from asic_flow.registry import add_plugin_paths, load_flow_class


class FlowExecutor:
    """Run enabled flows in dependency order using the configured plugins."""

    def __init__(self, manifest: Manifest, dry_run: bool = False) -> None:
        self.manifest = manifest
        self.context = FlowContext(
            project_name=manifest.project_name,
            manifest_path=manifest.path,
            project_root=manifest.project_root,
            workspace_root=manifest.workspace_root,
            logs_root=manifest.logs_root,
            env=manifest.env,
            project_env={},
            dry_run=dry_run,
        )
        add_plugin_paths(manifest.plugin_paths)

    def list_flows(self) -> list[FlowDefinition]:
        """Return only flows that are currently enabled."""

        return [flow for flow in self.manifest.flows.values() if flow.enabled]

    def run(self, targets: Iterable[str]) -> None:
        """Create runtime directories and execute each requested flow once."""

        self.context.workspace_root.mkdir(parents=True, exist_ok=True)
        self.context.logs_root.mkdir(parents=True, exist_ok=True)
        visited: set[str] = set()
        active: set[str] = set()
        for name in targets:
            self._run_one(name, visited, active)

    def _run_one(self, name: str, visited: set[str], active: set[str]) -> None:
        """Depth-first execution with cycle detection for dependencies."""

        if name in visited:
            return
        if name in active:
            cycle = " -> ".join([*active, name])
            raise ValueError(f"dependency cycle detected: {cycle}")

        definition = self.manifest.flows.get(name)
        if definition is None:
            raise ValueError(f"unknown flow: {name}")
        if not definition.enabled:
            raise ValueError(f"flow {name} is disabled")

        active.add(name)
        try:
            # Dependencies run before the requested flow, and `visited` keeps
            # shared dependencies from executing more than once.
            for dependency in definition.depends_on:
                self._run_one(dependency, visited, active)

            flow_class = load_flow_class(definition.plugin)
            flow = flow_class(definition, self.context)
            print(f"==> running flow: {name}")
            flow.run()
            visited.add(name)
        finally:
            active.remove(name)
