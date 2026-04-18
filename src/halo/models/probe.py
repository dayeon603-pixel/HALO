"""Layer 3 metacognition probe.

Tracks user-reported confidence against observed outcomes per sender. Builds
Brier-score calibration profile and relationship-anomaly signal used by the
risk engine.

Methodology transferred from MetaMirage (Kaggle AGI Benchmark Challenge 2026
Metacognition Track, submitted 2026-04-16 by the HALO team lead).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean
from typing import Literal

ActualOutcome = Literal["scam", "benign", "unknown"]


@dataclass(frozen=True, slots=True)
class ProbeRecord:
    """Single probe interaction."""

    sender_id_hash: str
    timestamp: datetime
    category: str
    user_confidence_1_to_10: int
    response_time_ms: int
    risk_score: int
    actual_outcome: ActualOutcome = "unknown"


@dataclass(slots=True)
class SenderProfile:
    """Per-sender accumulated probe history."""

    sender_id_hash: str
    probes: list[ProbeRecord] = field(default_factory=list)


class MetacognitionProbe:
    """Collects probe records and computes Brier score and anomaly signals.

    The probe fires when Layer 2 risk_score crosses the probe threshold. The
    UI elicits a 1~10 confidence response from the user. Results are recorded
    and, when the actual outcome becomes knowable, Brier scores are updated.
    """

    def __init__(self, probe_threshold: int = 50) -> None:
        self.probe_threshold = probe_threshold
        self._profiles: dict[str, SenderProfile] = defaultdict(
            lambda: SenderProfile(sender_id_hash="")
        )

    def record(self, record: ProbeRecord) -> None:
        """Persist a probe record into the in-memory store."""
        profile = self._profiles.setdefault(
            record.sender_id_hash,
            SenderProfile(sender_id_hash=record.sender_id_hash),
        )
        profile.probes.append(record)

    def resolve_outcome(
        self, sender_id_hash: str, timestamp: datetime, outcome: ActualOutcome
    ) -> None:
        """Update a prior probe with its resolved outcome."""
        raise NotImplementedError

    def brier_score(self, sender_id_hash: str) -> float:
        """Compute Brier score for a sender.

        Returns nan if no resolved outcomes exist.
        """
        profile = self._profiles.get(sender_id_hash)
        if profile is None:
            return float("nan")
        resolved = [p for p in profile.probes if p.actual_outcome != "unknown"]
        if not resolved:
            return float("nan")
        scores = [
            ((p.user_confidence_1_to_10 / 10.0) - (1.0 if p.actual_outcome == "benign" else 0.0)) ** 2
            for p in resolved
        ]
        return mean(scores)

    def user_overconfidence(self, sender_id_hash: str) -> float:
        """Derived signal for the risk engine. 0 means well-calibrated, 1 means maximally miscalibrated."""
        bs = self.brier_score(sender_id_hash)
        if bs != bs:
            return 0.0
        return max(0.0, min(1.0, bs * 4.0))

    def relationship_anomaly(self, sender_id_hash: str) -> float:
        """First-order derivative of the trust series, normalized.

        Sudden trust jumps after suspicious signals produce a positive value.
        Returns 0 if insufficient history.
        """
        raise NotImplementedError
