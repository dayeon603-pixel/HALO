"""Layer 2 scam classifier interface.

Defines the contract that all Layer 2 implementations satisfy:
    - Cloud prototype (Upstage Solar-pro via API, src/halo/demo/classifier_demo.py).
    - On-device production (KT Mi:dm 2.0 Mini with LoRA adapter).
    - Cross-lingual adapters (Phase 2, Japanese and English).

The Android app references this interface through ONNX Runtime Mobile;
language adapters are swapped by loading different LoRA weights at runtime.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

ScamCategory = Literal[
    "voice_phishing",
    "romance_scam",
    "investment_scam",
    "loan_scam",
    "subsidy_scam",
    "family_impersonation",
    "benign",
]


@dataclass(frozen=True, slots=True)
class ScamResult:
    """Classifier output consumed by Layer 3 and Layer 4.

    Attributes:
        category: Predicted scam category or benign.
        risk_score: Integer score from 0 (safe) to 100 (high risk).
        rationale: Short Korean justification shown to the user.
        key_signals: Three to five concrete signals.
        raw_logits: Optional per-category logits for calibration analysis.
    """

    category: ScamCategory
    risk_score: int
    rationale: str
    key_signals: list[str]
    raw_logits: dict[str, float] | None = None


class BaseScamClassifier(ABC):
    """Contract for Layer 2 classifiers. Either cloud or on-device."""

    @abstractmethod
    def classify(self, text: str) -> ScamResult:
        """Classify a single Korean message."""

    def classify_batch(self, texts: list[str]) -> list[ScamResult]:
        """Default implementation maps classify. Subclasses may override for efficiency."""
        return [self.classify(t) for t in texts]

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Canonical identifier for the backing model. Used in audit logs."""

    @property
    @abstractmethod
    def device(self) -> Literal["cpu", "gpu", "npu", "cloud"]:
        """Where inference runs."""


class SolarProApiClassifier(BaseScamClassifier):
    """Cloud prototype classifier using Upstage Solar-pro API.

    This is the demo-stage classifier. Production HALO replaces it with the
    on-device Mi:dm 2.0 Mini classifier once the LoRA adapter is trained.
    """

    def __init__(self, api_key: str, model: str = "solar-pro") -> None:
        self.api_key = api_key
        self._model = model

    def classify(self, text: str) -> ScamResult:
        raise NotImplementedError(
            "See src/halo/demo/classifier_demo.py for a working implementation."
        )

    @property
    def model_id(self) -> str:
        return f"upstage/{self._model}"

    @property
    def device(self) -> Literal["cloud"]:
        return "cloud"


class OnDeviceMidmClassifier(BaseScamClassifier):
    """Production on-device classifier using KT Mi:dm 2.0 Mini with LoRA adapter.

    Loaded as ONNX model via ONNX Runtime Mobile. The Android app provides
    QNN or NNAPI delegate depending on hardware.
    """

    def __init__(
        self,
        onnx_model_path: str,
        lora_adapter_path: str,
        tokenizer_path: str,
    ) -> None:
        self.onnx_model_path = onnx_model_path
        self.lora_adapter_path = lora_adapter_path
        self.tokenizer_path = tokenizer_path

    def classify(self, text: str) -> ScamResult:
        raise NotImplementedError(
            "Production inference wired in Android native layer. "
            "Python-side stub for schema reference."
        )

    @property
    def model_id(self) -> str:
        return "kt/midm-2.0-mini+halo-lora"

    @property
    def device(self) -> Literal["npu"]:
        return "npu"
