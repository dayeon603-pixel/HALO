"""Tests for halo.models.risk."""

import pytest

from halo.models.classifier import ScamResult
from halo.models.probe import MetacognitionProbe
from halo.models.risk import RiskEngine, RiskWeights, intervention_level


def test_intervention_level_thresholds() -> None:
    assert intervention_level(0) == "none"
    assert intervention_level(49) == "none"
    assert intervention_level(50) == "soft"
    assert intervention_level(74) == "soft"
    assert intervention_level(75) == "medium"
    assert intervention_level(89) == "medium"
    assert intervention_level(90) == "hard"
    assert intervention_level(100) == "hard"


def test_risk_weights_sum_sensible() -> None:
    w = RiskWeights()
    assert pytest.approx(w.sum(), rel=1e-6) == 1.0


def test_risk_computation_uses_pattern_weight() -> None:
    probe = MetacognitionProbe()
    engine = RiskEngine(probe=probe, weights=RiskWeights(1.0, 0.0, 0.0))
    result = ScamResult(
        category="voice_phishing",
        risk_score=80,
        rationale="기관 사칭",
        key_signals=["수사기관 사칭"],
    )
    assert engine.compute("sender-hash-abc", result) == 80


def test_risk_bounded_to_100() -> None:
    probe = MetacognitionProbe()
    engine = RiskEngine(probe=probe, weights=RiskWeights(2.0, 0.0, 0.0))
    result = ScamResult(
        category="voice_phishing",
        risk_score=80,
        rationale="",
        key_signals=[],
    )
    assert engine.compute("sender-hash-def", result) == 100
