"""Risk scoring engine combining Layer 2 pattern score and Layer 3 signals."""

from __future__ import annotations

from dataclasses import dataclass

from halo.models.classifier import ScamResult
from halo.models.probe import MetacognitionProbe


@dataclass(frozen=True, slots=True)
class RiskWeights:
    """Linear weights for the three signals in the risk formula."""

    alpha_pattern: float = 0.5
    beta_overconfidence: float = 0.3
    gamma_relationship_anomaly: float = 0.2

    def sum(self) -> float:
        return self.alpha_pattern + self.beta_overconfidence + self.gamma_relationship_anomaly


class RiskEngine:
    """Combines pattern, overconfidence, and relationship-anomaly signals.

    Formula:
        Risk = alpha * PatternScore
             + beta  * UserOverconfidence * 100
             + gamma * RelationshipAnomaly * 100

    Range: 0 to 100.
    """

    def __init__(self, probe: MetacognitionProbe, weights: RiskWeights | None = None) -> None:
        self.probe = probe
        self.weights = weights or RiskWeights()

    def compute(self, sender_id_hash: str, classification: ScamResult) -> int:
        """Compute final risk score."""
        pattern = classification.risk_score
        overconfidence = self.probe.user_overconfidence(sender_id_hash) * 100.0
        anomaly = self._safe_relationship_anomaly(sender_id_hash) * 100.0
        combined = (
            self.weights.alpha_pattern * pattern
            + self.weights.beta_overconfidence * overconfidence
            + self.weights.gamma_relationship_anomaly * anomaly
        )
        return int(round(max(0.0, min(100.0, combined))))

    def _safe_relationship_anomaly(self, sender_id_hash: str) -> float:
        try:
            return self.probe.relationship_anomaly(sender_id_hash)
        except NotImplementedError:
            return 0.0


def intervention_level(risk: int) -> str:
    """Map risk score to intervention level per docs/architecture.md §Layer 4."""
    if risk >= 90:
        return "hard"
    if risk >= 75:
        return "medium"
    if risk >= 50:
        return "soft"
    return "none"
