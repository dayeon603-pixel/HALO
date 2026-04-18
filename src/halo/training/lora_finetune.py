"""LoRA fine-tuning of KT Mi:dm 2.0 Mini on the Korean scam corpus.

Usage:
    halo-train --config configs/model_midm_mini.yaml

Workflow:
    1. Load K-intelligence/Midm-2.0-Base-Instruct from HuggingFace.
    2. Apply LoRA config (rank 16, alpha 32, target_modules q/k/v/o_proj).
    3. Tokenize ScamCorpusRow entries into Mi:dm format with instruction
       template that requests JSON output.
    4. Train for 3 epochs with bf16 mixed precision.
    5. Evaluate on held-out test set.
    6. Save LoRA adapter to out_dir/adapter.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from loguru import logger


@dataclass
class FineTuneConfig:
    base_model_id: str = "K-intelligence/Midm-2.0-Base-Instruct"
    corpus_path: Path = Path("data/processed/corpus_v1.parquet")
    output_dir: Path = Path("artifacts/lora_adapter_v0")

    lora_rank: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: tuple[str, ...] = ("q_proj", "v_proj", "k_proj", "o_proj")

    learning_rate: float = 1e-4
    num_epochs: int = 3
    per_device_batch_size: int = 4
    gradient_accumulation_steps: int = 4
    warmup_ratio: float = 0.1
    lr_scheduler: str = "cosine"

    max_seq_length: int = 512
    seed: int = 42
    mixed_precision: str = "bf16"

    wandb_project: str = "halo"


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True


def build_instruction(text: str) -> str:
    """Format a corpus row into the Mi:dm instruction template.

    Matches the system prompt used in src/halo/demo/classifier_demo.py.
    """
    raise NotImplementedError


def train(config: FineTuneConfig) -> Path:
    """Run LoRA fine-tuning and return the adapter output directory.

    Args:
        config: Training configuration.

    Returns:
        Path to saved LoRA adapter.
    """
    set_seed(config.seed)
    logger.info("Starting HALO LoRA fine-tune: model={}, corpus={}", config.base_model_id, config.corpus_path)
    raise NotImplementedError


def main() -> None:
    """CLI entry point. Parses args and invokes train()."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
