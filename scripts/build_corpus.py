#!/usr/bin/env python3
"""Build the Korean scam corpus from configured sources.

Example:
    python scripts/build_corpus.py \
        --sources police,kisa,community \
        --output data/processed/corpus_v0.parquet \
        --seed 42

Outputs a Parquet file that conforms to ScamCorpusSchema. Safe to run
repeatedly; existing entries are deduplicated by (source_ref, text_hash).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loguru import logger

from halo.corpus.collectors import (
    CommunityPostCollector,
    KisaAdvisoryCollector,
    PoliceReleaseCollector,
)

SOURCES = {
    "police": PoliceReleaseCollector,
    "kisa": KisaAdvisoryCollector,
    "community": CommunityPostCollector,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--sources",
        type=str,
        default="police,kisa",
        help="Comma-separated list of sources. Options: %(choices)s",
        choices=list(SOURCES.keys()),
    )
    p.add_argument("--output", type=Path, required=True, help="Output Parquet path")
    p.add_argument("--cache-dir", type=Path, default=Path("data/raw/_cache"))
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-rows", type=int, default=10_000)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    logger.info("Building corpus from sources={} seed={}", sources, args.seed)

    for source in sources:
        if source not in SOURCES:
            logger.error("Unknown source: {}. Valid: {}", source, list(SOURCES.keys()))
            return 2
        logger.info("Collector {} would run here (not yet implemented)", source)

    logger.info("Corpus build skeleton ready. Wire in M1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
