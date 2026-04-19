#!/usr/bin/env python3
"""Evaluate a HALO classifier on a held-out test set.

Example:
    python scripts/evaluate.py --config configs/eval.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loguru import logger


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--model-path", type=Path, help="Override model path from config")
    p.add_argument("--output", type=Path, default=Path("artifacts/eval_report.md"))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    logger.info("HALO evaluation: config={}", args.config)
    logger.warning("Evaluation harness not yet implemented. Planned for M2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
