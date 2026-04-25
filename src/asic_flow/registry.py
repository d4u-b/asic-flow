from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Type

from asic_flow.flows.base import BaseFlow


def add_plugin_paths(paths: list[Path]) -> None:
    """Prepend plugin search paths so project-local flows can be imported."""

    for path in reversed(paths):
        value = str(path)
        if value not in sys.path:
            sys.path.insert(0, value)


def load_flow_class(target: str) -> Type[BaseFlow]:
    """Import a `module:ClassName` plugin target and validate its type."""

    module_name, separator, class_name = target.partition(":")
    if not separator or not class_name:
        raise ValueError(f"invalid plugin target: {target}")

    module = importlib.import_module(module_name)
    flow_class = getattr(module, class_name, None)
    if flow_class is None:
        raise ValueError(f"plugin class not found: {target}")
    if not isinstance(flow_class, type) or not issubclass(flow_class, BaseFlow):
        raise ValueError(f"plugin {target} must inherit from BaseFlow")
    return flow_class
