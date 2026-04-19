#!/usr/bin/env python3
"""Fine-tune KT Mi:dm 2.0 Mini with LoRA on the Korean scam corpus.

Example:
    python scripts/train.py --config configs/model_midm_mini.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loguru import logger


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, required=True, help="Hydra YAML config")
    p.add_argument("--output-dir", type=Path, default=Path("artifacts/lora_adapter_v0"))
    p.add_argument("--wandb", action="store_true", help="Enable W&B tracking")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    logger.info("HALO LoRA training: config={} output={}", args.config, args.output_dir)
    logger.warning("Training pipeline not yet implemented. Planned for M2 (2026-07).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
