# Metacognition Probe: Methodology Transfer from MetaMirage

Layer 3 of HALO builds on MetaMirage, the research submitted by the author to
Google DeepMind × Kaggle AGI Benchmark Challenge 2026 Metacognition Track on
2026-04-16. This document describes the transfer methodology, its hypothesis
structure, and the fallback design.

## Origin: MetaMirage

MetaMirage studied the relationship between language model capability and
metacognitive accuracy on engineered task families.

Finding: models of higher capability show lower metacognitive accuracy on
these engineered families.

Quantitative summary:
- Correlation coefficient: r = -0.84
- Sample size: n = 7 model checkpoints
- p-value: approximately 0.02
- 95% confidence interval: r ∈ [-0.97, -0.31]

Interpretation: the effect is preliminary. n = 7 is small, the CI is wide,
and transfer to human users is not demonstrated. MetaMirage provides a
methodology, not a proven human phenomenon.

## Transfer hypothesis (exploratory)

Hypothesis H_transfer: human users exhibit a measurable calibration gap
between self-reported confidence in a message sender and the actual outcome
of interactions with that sender.

Operational translation:
- For each interaction, record the user's verbalized confidence (1~10).
- After the interaction resolves (e.g. the user reports that the sender was
  scam or not), compute a per-user Brier score across past probes.
- If Brier scores remain high (poor calibration) and do not improve over
  time, the user has a persistent metacognitive gap that HALO can help close.

H_transfer is exploratory. The pilot in M4~M6 tests it on 5~10 elder users at
성남시 어르신복지관.

## Probe protocol

Trigger: Layer 2 produces `risk_score ≥ 50` for an incoming message.

Display:
1. Full-screen overlay with the rationale and key signals from Layer 2.
2. Single probe question in large Korean text:
   "이 사람(발신자)을 얼마나 믿으세요? 1(전혀 아님) ~ 10(완전히)"
3. Large tap targets (10 numbered buttons) for accessibility.

Recording:
```python
ProbeRecord(
    sender_id_hash: str,      # salted
    timestamp: datetime,
    category: str,            # from Layer 2
    user_confidence: int,     # 1~10
    response_time_ms: int,
    risk_score: int,          # from Layer 2
    actual_outcome: Optional[str],  # "scam" | "benign" | None, resolved later
)
```

## Brier score computation

Given a probe history for a sender over N interactions, the user's Brier score
is:

```
BS = (1 / N) * sum(
    (normalized_confidence_i - actual_outcome_i)^2
)
```

Where `normalized_confidence = confidence / 10` (range 0~1) and
`actual_outcome = 1 if benign else 0`.

Lower BS means better calibration. A BS at or above 0.25 (the random-baseline
expectation) indicates poor calibration.

## Relationship anomaly component

For sustained relationships (romance scam, investment scam), we track the
trust time series per sender:

```
trust_t = user_confidence_t / 10
```

Anomaly signal (simple first-order derivative):
```
anomaly_t = (trust_t - trust_{t-1}) - mean_change
```

Sudden trust jumps after observing suspicious signals trigger Layer 3
elevation.

## Risk combination

```
Risk_total = α · PatternScore + β · UserOverconfidence + γ · RelationshipAnomaly
```

Initial weights: α = 0.5, β = 0.3, γ = 0.2. Updated after M5 pilot data
collection using grid search on withheld pilot users.

`UserOverconfidence` is defined as `1 - BrierScore` clamped to [0, 1].

## Fallback: Bayesian calibration without transfer hypothesis

If the pilot rejects H_transfer, Layer 3 does not collapse. We replace the
Brier-score-based overconfidence term with a simple Bayesian prior update:

```
P(scam | sender_history) = (n_past_scam + 1) / (n_past_total + 2)
```

This produces a calibrated probability purely from observed past behavior,
without requiring the metacognition transfer to hold.

The architecture is designed so that Layer 3 functions as an informed prior
update engine regardless of whether H_transfer replicates in humans.

## Open experimental questions (for M4 pilot)

1. Do elder users produce interpretable confidence responses on a 1~10 scale?
2. Does response time correlate with true uncertainty?
3. Does confidence calibration improve over the pilot period with HALO feedback?
4. Does Layer 3 elevation reduce actual scam incidents vs Soft-only Layer 2?

## References

- MetaMirage submission, Kaggle AGI Benchmark Challenge 2026 Metacognition Track, 2026-04-16.
- Brier, G.W. (1950). Verification of Forecasts Expressed in Terms of Probability.
- Dawid, A.P. (1982). The Well-Calibrated Bayesian.
