#!/usr/bin/env python3
"""Sanity check the local HALO development environment.

Verifies that required Python version, packages, and optional tools are
available before running training or evaluation.

Example:
    python scripts/check_env.py
"""

from __future__ import annotations

import importlib
import os
import shutil
import sys
from dataclasses import dataclass

REQUIRED_PACKAGES = [
    "torch",
    "transformers",
    "peft",
    "loguru",
    "pydantic",
    "pandera",
    "pandas",
    "numpy",
]

OPTIONAL_TOOLS = ["git", "pre-commit", "ruff", "black", "mypy"]


@dataclass(frozen=True, slots=True)
class CheckResult:
    name: str
    ok: bool
    detail: str


def check_python() -> CheckResult:
    ok = sys.version_info >= (3, 11)
    return CheckResult(
        name="python>=3.11",
        ok=ok,
        detail=f"found {sys.version.split()[0]}",
    )


def check_package(name: str) -> CheckResult:
    try:
        mod = importlib.import_module(name)
        version = getattr(mod, "__version__", "unknown")
        return CheckResult(name=f"package:{name}", ok=True, detail=f"version {version}")
    except ImportError:
        return CheckResult(name=f"package:{name}", ok=False, detail="not installed")


def check_tool(name: str) -> CheckResult:
    path = shutil.which(name)
    return CheckResult(
        name=f"tool:{name}",
        ok=path is not None,
        detail=path or "not found",
    )


def check_env_var(name: str, required: bool = False) -> CheckResult:
    value = os.environ.get(name)
    present = value is not None and value != ""
    ok = present or not required
    detail = "set" if present else "unset"
    return CheckResult(name=f"env:{name}", ok=ok, detail=detail)


def main() -> int:
    results: list[CheckResult] = []
    results.append(check_python())
    results.extend(check_package(p) for p in REQUIRED_PACKAGES)
    results.extend(check_tool(t) for t in OPTIONAL_TOOLS)
    results.append(check_env_var("UPSTAGE_API_KEY", required=False))
    results.append(check_env_var("WANDB_API_KEY", required=False))

    failures = [r for r in results if not r.ok]
    for r in results:
        mark = "OK" if r.ok else "FAIL"
        print(f"[{mark:4}] {r.name:30} {r.detail}")

    if failures:
        print(f"\n{len(failures)} check(s) failed.")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
