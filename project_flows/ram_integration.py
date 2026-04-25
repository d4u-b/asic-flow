from __future__ import annotations

from pathlib import Path

from asic_flow.flows.base import BaseFlow


class RamPrepFlow(BaseFlow):
    """Demo flow for RAM generation and stale-artifact cleanup."""

    def run(self) -> None:
        options = self.definition.options
        config_path = self.context.resolve_path(options.get("config", "config/ram_blocks.yaml"))
        generated_root = self.context.resolve_path(options.get("generated_root", "build/ram"))
        reports_root = self.context.resolve_path(options.get("reports_root", "reports/ram"))
        manifest_name = options.get("artifact_manifest", "generated_rams.txt")

        generated_root.mkdir(parents=True, exist_ok=True)
        reports_root.mkdir(parents=True, exist_ok=True)

        if not config_path.exists():
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(
                "# Demo RAM generator input\n"
                "rams:\n"
                "  - name: icache_ram\n"
                "    depth: 1024\n"
                "    width: 64\n"
                "  - name: dcache_ram\n"
                "    depth: 2048\n"
                "    width: 64\n",
                encoding="utf-8",
            )

        stale_dir = generated_root / "stale"
        if stale_dir.exists():
            for path in sorted(stale_dir.rglob("*"), reverse=True):
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    path.rmdir()
            stale_dir.rmdir()

        manifest_path = reports_root / manifest_name
        ram_names = ["icache_ram", "dcache_ram"]

        for ram_name in ram_names:
            for suffix, body in (
                (".sv", f"// demo RTL model for {ram_name}\n"),
                (".lib", f"# demo liberty view for {ram_name}\n"),
                (".lef", f"# demo LEF view for {ram_name}\n"),
                (".gds", f"demo GDS placeholder for {ram_name}\n"),
            ):
                artifact = generated_root / f"{ram_name}{suffix}"
                artifact.write_text(body, encoding="utf-8")

        manifest_path.write_text(
            "\n".join(str(generated_root / f"{ram_name}.sv") for ram_name in ram_names) + "\n",
            encoding="utf-8",
        )

        summary_path = reports_root / "ram_prep.txt"
        summary_path.write_text(
            "Demo RAM preparation complete\n"
            f"config={config_path}\n"
            f"generated_root={generated_root}\n"
            f"artifact_manifest={manifest_path}\n",
            encoding="utf-8",
        )


class RamCollateralFlow(BaseFlow):
    """Demo flow for rebuilding RAM filelists after generation."""

    def run(self) -> None:
        options = self.definition.options
        generated_root = self.context.resolve_path(options.get("generated_root", "build/ram"))
        filelist_root = self.context.resolve_path(options.get("filelist_root", "filelists"))
        reports_root = self.context.resolve_path(options.get("reports_root", "reports/ram"))

        filelist_root.mkdir(parents=True, exist_ok=True)
        reports_root.mkdir(parents=True, exist_ok=True)

        sv_files = sorted(generated_root.glob("*.sv"))
        lib_files = sorted(generated_root.glob("*.lib"))

        if not sv_files or not lib_files:
            raise ValueError(f"expected generated RAM collateral under {generated_root}")

        sv_f = filelist_root / "ram_rtl.f"
        lib_f = filelist_root / "ram_lib.f"
        sv_f.write_text("\n".join(str(path) for path in sv_files) + "\n", encoding="utf-8")
        lib_f.write_text("\n".join(str(path) for path in lib_files) + "\n", encoding="utf-8")

        summary_path = reports_root / "ram_collateral.txt"
        summary_path.write_text(
            "Demo RAM collateral refresh complete\n"
            f"rtl_filelist={sv_f}\n"
            f"lib_filelist={lib_f}\n",
            encoding="utf-8",
        )
