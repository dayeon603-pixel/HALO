"""Evaluation harness for HALO Layer 2 classifier.

Computes per-category F1, precision, recall, ECE, and latency metrics on a
held-out test set and, optionally, on pilot-derived real-world data.

Usage:
    halo-evaluate --model artifacts/lora_adapter_v0 --split test
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

from halo.models.classifier import BaseScamClassifier, ScamResult


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """Aggregated evaluation output."""

    per_category_f1: dict[str, float]
    per_category_precision: dict[str, float]
    per_category_recall: dict[str, float]
    macro_f1: float
    ece: float
    false_positive_rate_benign: float
    latency_p50_ms: float
    latency_p95_ms: float
    n_samples: int


def run(
    classifier: BaseScamClassifier, test_df: pd.DataFrame, device: str = "cuda"
) -> EvaluationResult:
    """Run evaluation.

    Args:
        classifier: A BaseScamClassifier implementation.
        test_df: DataFrame conforming to ScamCorpusSchema.
        device: Hardware identifier for logging.

    Returns:
        EvaluationResult.
    """
    logger.info("Starting evaluation: n={}, device={}", len(test_df), device)
    raise NotImplementedError


def expected_calibration_error(
    confidences: np.ndarray, correct: np.ndarray, n_bins: int = 10
) -> float:
    """Compute Expected Calibration Error.

    Args:
        confidences: Array of predicted confidences in [0, 1].
        correct: Array of 0/1 correctness indicators.
        n_bins: Histogram bins.

    Returns:
        ECE in [0, 1]. Lower is better.
    """
    raise NotImplementedError


def report_markdown(result: EvaluationResult) -> str:
    """Format EvaluationResult as a markdown table for reporting."""
    raise NotImplementedError


def main() -> None:
    """CLI entry point."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
