"""Export LoRA-tuned Mi:dm 2.0 Mini to ONNX for mobile deployment.

Pipeline:
    1. Load base Mi:dm 2.0 Mini model.
    2. Merge LoRA adapter weights into base.
    3. Export to ONNX via Optimum with opset 17.
    4. Apply GPTQ INT4 quantization.
    5. Verify output equivalence against HuggingFace model on a small test set.

Usage:
    halo-export-mobile --adapter artifacts/lora_adapter_v0 --out artifacts/halo_midm_mini.onnx
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from loguru import logger


@dataclass(frozen=True, slots=True)
class ExportConfig:
    base_model_id: str = "K-intelligence/Midm-2.0-Base-Instruct"
    lora_adapter_path: Path = Path("artifacts/lora_adapter_v0")
    output_onnx_path: Path = Path("artifacts/halo_midm_mini.onnx")
    opset: int = 17
    quantization: str = "gptq_int4"
    verify_samples: int = 20


def merge_and_export(config: ExportConfig) -> Path:
    """Merge LoRA adapter into base model and export to ONNX with quantization.

    Args:
        config: Export configuration.

    Returns:
        Path to the final quantized ONNX file.
    """
    logger.info("Merging LoRA adapter and exporting ONNX to {}", config.output_onnx_path)
    raise NotImplementedError


def verify_equivalence(
    onnx_path: Path, hf_model_id: str, lora_adapter_path: Path, n_samples: int = 20
) -> bool:
    """Verify that the ONNX model reproduces HuggingFace predictions within tolerance.

    Returns True if all samples match. Raises with diagnostic info on mismatch.
    """
    raise NotImplementedError


def main() -> None:
    """CLI entry point."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
