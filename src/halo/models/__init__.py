"""Model definitions for HALO layers 2 and 3.

Modules:
    classifier  Layer 2 six-plus-one category scam classifier interface.
    probe       Layer 3 metacognition probe and Brier score tracking.
    risk        Risk scoring engine combining Layers 2 and 3.
"""

from halo.models.classifier import BaseScamClassifier, ScamResult
from halo.models.probe import MetacognitionProbe, ProbeRecord
from halo.models.risk import RiskEngine, RiskWeights

__all__ = [
    "BaseScamClassifier",
    "MetacognitionProbe",
    "ProbeRecord",
    "RiskEngine",
    "RiskWeights",
    "ScamResult",
]
