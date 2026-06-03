#!/usr/bin/env python3
"""Convenience entry point for regenerating plot files from CSV data."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    script = ROOT / "scripts" / "generate_verified_outputs.ps1"
    subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script)],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
