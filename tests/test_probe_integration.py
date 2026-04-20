"""Integration tests for metacognition probe and risk engine interaction."""

from datetime import datetime, timezone

from halo.models.classifier import ScamResult
from halo.models.probe import MetacognitionProbe, ProbeRecord
from halo.models.risk import RiskEngine, RiskWeights, intervention_level


def _probe_record(sender: str, confidence: int, outcome: str = "unknown") -> ProbeRecord:
    return ProbeRecord(
        sender_id_hash=sender,
        timestamp=datetime(2026, 4, 21, tzinfo=timezone.utc),
        category="voice_phishing",
        user_confidence_1_to_10=confidence,
        response_time_ms=2500,
        risk_score=70,
        actual_outcome=outcome,  # type: ignore[arg-type]
    )


def test_probe_records_persist() -> None:
    probe = MetacognitionProbe()
    probe.record(_probe_record("sender-a", 8))
    probe.record(_probe_record("sender-a", 6))
    profile = probe._profiles["sender-a"]
    assert len(profile.probes) == 2


def test_brier_score_nan_without_resolved_outcomes() -> None:
    probe = MetacognitionProbe()
    probe.record(_probe_record("sender-b", 7))
    score = probe.brier_score("sender-b")
    assert score != score  # NaN test


def test_brier_score_unknown_sender_is_nan() -> None:
    probe = MetacognitionProbe()
    score = probe.brier_score("never-seen")
    assert score != score


def test_user_overconfidence_defaults_to_zero() -> None:
    probe = MetacognitionProbe()
    assert probe.user_overconfidence("sender-c") == 0.0


def test_risk_engine_returns_bounded_value() -> None:
    probe = MetacognitionProbe()
    engine = RiskEngine(probe=probe, weights=RiskWeights(0.5, 0.3, 0.2))
    classification = ScamResult(
        category="voice_phishing",
        risk_score=72,
        rationale="기관 사칭 + 긴급 이체 유도",
        key_signals=["수사기관 사칭", "이체 유도"],
    )
    risk = engine.compute("sender-d", classification)
    assert 0 <= risk <= 100


def test_intervention_levels_cover_full_range() -> None:
    levels = {intervention_level(r) for r in range(0, 101, 5)}
    assert levels == {"none", "soft", "medium", "hard"}


def test_pure_pattern_weighting_matches_pattern_score() -> None:
    probe = MetacognitionProbe()
    engine = RiskEngine(probe=probe, weights=RiskWeights(1.0, 0.0, 0.0))
    classification = ScamResult(
        category="benign",
        risk_score=15,
        rationale="일반 메시지",
        key_signals=[],
    )
    assert engine.compute("sender-e", classification) == 15
