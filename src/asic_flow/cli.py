from __future__ import annotations

import argparse
from pathlib import Path

from asic_flow.config import load_manifest
from asic_flow.executor import FlowExecutor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ASIC flow controller")
    parser.add_argument(
        "--manifest",
        default="project.toml",
        help="Path to the flow manifest file",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List enabled flows")
    list_parser.add_argument("--details", action="store_true", help="Show dependencies and plugin target")

    run_parser = subparsers.add_parser("run", help="Run one or more flows")
    run_parser.add_argument("flows", nargs="*", help="Flow names to run")
    run_parser.add_argument("--all", action="store_true", help="Run all enabled flows")
    run_parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them")

    return parser


def _load_executor(manifest_arg: str, dry_run: bool = False) -> FlowExecutor:
    manifest = load_manifest(Path(manifest_arg))
    return FlowExecutor(manifest, dry_run=dry_run)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        executor = _load_executor(args.manifest)
        for flow in executor.list_flows():
            if args.details:
                deps = ", ".join(flow.depends_on) if flow.depends_on else "-"
                print(f"{flow.name:12} deps={deps:16} plugin={flow.plugin}")
            else:
                print(flow.name)
        return 0

    if args.command == "run":
        executor = _load_executor(args.manifest, dry_run=args.dry_run)
        if args.all:
            targets = [flow.name for flow in executor.list_flows()]
        else:
            targets = args.flows
        if not targets:
            parser.error("run requires flow names or --all")
        executor.run(targets)
        return 0

    parser.error(f"unsupported command: {args.command}")
    return 2
