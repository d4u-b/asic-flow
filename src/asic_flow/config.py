from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class FlowDefinition:
    """Normalized configuration for a single flow entry in the manifest."""

    name: str
    plugin: str
    description: str = ""
    depends_on: list[str] = field(default_factory=list)
    enabled: bool = True
    workdir: str | None = None
    commands: list[list[str]] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    options: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Manifest:
    """Resolved project configuration consumed by the executor."""

    path: Path
    project_name: str
    project_root: Path
    workspace_root: Path
    logs_root: Path
    env: dict[str, str]
    plugin_paths: list[Path]
    flows: dict[str, FlowDefinition]


def _read_toml(path: Path) -> dict[str, Any]:
    """Load a TOML manifest from disk."""

    with path.open("rb") as handle:
        return tomllib.load(handle)


def _read_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML manifest when PyYAML is available."""

    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError(
            "YAML manifest support requires PyYAML. Install it with `python3 -m pip install PyYAML`."
        ) from exc

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError("YAML manifest root must be a mapping")
    return data


def _read_manifest(path: Path) -> dict[str, Any]:
    """Dispatch to the parser that matches the manifest file extension."""

    suffix = path.suffix.lower()
    if suffix == ".toml":
        return _read_toml(path)
    if suffix in {".yaml", ".yml"}:
        return _read_yaml(path)
    raise ValueError(f"unsupported manifest format: {path.name}")


def _merge_mapping(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge manifest mappings with later values taking precedence."""

    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _merge_mapping(merged[key], value)
        else:
            merged[key] = value
    return merged


def _as_list_of_str(name: str, values: Any) -> list[str]:
    """Validate a manifest field that must be a list of strings."""

    if values is None:
        return []
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise ValueError(f"{name} must be a list of strings")
    return values


def _as_commands(values: Any) -> list[list[str]]:
    """Validate command arrays as a list of argv-style string lists."""

    if values is None:
        return []
    if not isinstance(values, list):
        raise ValueError("commands must be a list")
    commands: list[list[str]] = []
    for index, command in enumerate(values):
        if not isinstance(command, list) or not command or not all(isinstance(part, str) for part in command):
            raise ValueError(f"commands[{index}] must be a non-empty list of strings")
        commands.append(command)
    return commands


def _load_manifest_tree(path: Path, stack: tuple[Path, ...] = ()) -> dict[str, Any]:
    """Load a manifest plus its includes into one raw manifest mapping."""

    resolved = path.resolve()
    if resolved in stack:
        chain = " -> ".join(str(item) for item in (*stack, resolved))
        raise ValueError(f"manifest include cycle detected: {chain}")

    raw = _read_manifest(resolved)
    include_paths = _as_list_of_str("include", raw.get("include", []))

    merged: dict[str, Any] = {}
    for include_name in include_paths:
        child = _load_manifest_tree(resolved.parent / include_name, (*stack, resolved))
        merged = _merge_mapping(merged, {key: value for key, value in child.items() if key != "flow"})
        child_flows = child.get("flow", [])
        if child_flows:
            merged.setdefault("flow", [])
            if not isinstance(merged["flow"], list):
                raise ValueError("merged flow section must be a list")
            merged["flow"].extend(child_flows)

    merged = _merge_mapping(merged, {key: value for key, value in raw.items() if key not in {"include", "flow"}})

    current_flows = raw.get("flow", [])
    if current_flows:
        if not isinstance(current_flows, list):
            raise ValueError("flow must be an array of tables")
        merged.setdefault("flow", [])
        if not isinstance(merged["flow"], list):
            raise ValueError("merged flow section must be a list")
        merged["flow"].extend(current_flows)

    return merged


def load_manifest(path: str | Path) -> Manifest:
    """Parse the manifest file and resolve paths relative to the project root."""

    manifest_path = Path(path).expanduser().resolve()
    raw = _load_manifest_tree(manifest_path)

    project = raw.get("project", {})
    runtime = raw.get("runtime", {})
    defaults = raw.get("defaults", {})

    if not isinstance(project, dict) or not isinstance(runtime, dict) or not isinstance(defaults, dict):
        raise ValueError("project, runtime, and defaults sections must be mappings")

    project_name = project.get("name", manifest_path.stem)
    if not isinstance(project_name, str):
        raise ValueError("project.name must be a string")

    project_root = manifest_path.parent.resolve()
    workspace_root = (project_root / runtime.get("workspace_root", "work")).resolve()
    logs_root = (project_root / runtime.get("logs_root", "logs")).resolve()

    plugin_paths = []
    for item in _as_list_of_str("runtime.plugin_paths", runtime.get("plugin_paths", [])):
        plugin_paths.append((project_root / item).resolve())

    env = runtime.get("env", {})
    if not isinstance(env, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items()):
        raise ValueError("runtime.env must be a mapping of string values")

    raw_flows = raw.get("flow", [])
    if not isinstance(raw_flows, list):
        raise ValueError("flow must be an array of tables")

    flows: dict[str, FlowDefinition] = {}
    default_plugin = defaults.get("plugin", "asic_flow.flows.builtin:CommandFlow")
    default_workdir = defaults.get("workdir")

    for entry in raw_flows:
        if not isinstance(entry, dict):
            raise ValueError("each flow entry must be a table")
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("each flow must have a non-empty string name")
        if name in flows:
            raise ValueError(f"duplicate flow name: {name}")

        plugin = entry.get("plugin", default_plugin)
        if not isinstance(plugin, str):
            raise ValueError(f"flow {name}: plugin must be a string")

        description = entry.get("description", "")
        if not isinstance(description, str):
            raise ValueError(f"flow {name}: description must be a string")

        enabled = entry.get("enabled", True)
        if not isinstance(enabled, bool):
            raise ValueError(f"flow {name}: enabled must be a boolean")

        flow_env = entry.get("env", {})
        if not isinstance(flow_env, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in flow_env.items()):
            raise ValueError(f"flow {name}: env must be a mapping of string values")

        options = entry.get("options", {})
        if not isinstance(options, dict):
            raise ValueError(f"flow {name}: options must be a mapping")

        # Each flow is normalized once here so the executor can operate on a
        # consistent in-memory model without re-validating user input later.
        flows[name] = FlowDefinition(
            name=name,
            plugin=plugin,
            description=description,
            depends_on=_as_list_of_str(f"flow {name}.depends_on", entry.get("depends_on", [])),
            enabled=enabled,
            workdir=entry.get("workdir", default_workdir),
            commands=_as_commands(entry.get("commands", [])),
            env=flow_env,
            inputs=_as_list_of_str(f"flow {name}.inputs", entry.get("inputs", [])),
            outputs=_as_list_of_str(f"flow {name}.outputs", entry.get("outputs", [])),
            tags=_as_list_of_str(f"flow {name}.tags", entry.get("tags", [])),
            options=options,
        )

    return Manifest(
        path=manifest_path,
        project_name=project_name,
        project_root=project_root,
        workspace_root=workspace_root,
        logs_root=logs_root,
        env=env,
        plugin_paths=plugin_paths,
        flows=flows,
    )
