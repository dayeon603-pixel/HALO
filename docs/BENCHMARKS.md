# HALO Benchmarks

Timestamped measurements of HALO performance. This document is append-only
and tracks the progression from cloud prototype to on-device production.

## Layer 2 Classifier

### Baseline v0.1 — Solar-pro API (2026-04-20)

Environment: cloud, Upstage Solar API, default parameters.
Sample battery: 25 synthetic Korean messages across 6+1 categories,
including 4 adversarial variants. Raw results at
`experiments/baseline_v0_solar_pro/`.

| Metric | Value | Target |
|---|---|---|
| Macro F1 | 0.880 | reference |
| Primary 3-category F1 mean | **0.869** | ≥ 0.82 (clears) |
| Overall accuracy | 88.0 % | — |
| Adversarial accuracy (4 variants) | 4 / 4 = 100 % | — |
| Latency p50 | 899 ms | — |
| Latency p95 | 1418 ms | — |

Notes:
- Three errors were all hybrid-category boundary cases (voice↔family,
  voice↔subsidy, romance↔investment). These motivate Layer 3 metacognition
  probe rather than additional Layer 2 tuning alone.
- Secondary run with `solar-mini` produced identical F1 0.869 but higher
  latency (p50 1392 ms), so `solar-pro` is retained as the cloud reference.

### Baseline v0.2 — Solar-pro API, expanded corpus (2026-04-21)

Environment: cloud, Upstage Solar API.
Sample battery: 60 synthetic Korean messages across 6+1 categories,
including 17 adversarial variants (emoji spacing, character substitution,
similar domain, compressed, hanja/domain mixing, star obfuscation, jamo
split, unicode homoglyph, code-mix). See
`src/halo/demo/classifier_demo.py::SAMPLE_MESSAGES`.

Expected F1 movement: with n=60 vs n=25, per-category samples roughly
double (5 to 8 per class plus adversarial). Expected primary F1 remains
near 0.85 with tighter confidence interval.

**How to reproduce:**
```bash
export UPSTAGE_API_KEY=<key>
cd ~/halo
python -m halo.demo.classifier_demo \
    --report experiments/baseline_v0.2_solar_pro/report.md \
    --json experiments/baseline_v0.2_solar_pro/results.json
```

### Planned — Mi:dm 2.0 Mini on-device (M2, 2026-07)

Environment: Galaxy S24, Snapdragon 8 Gen 3, ONNX Runtime Mobile 1.24,
Qualcomm QNN delegate. INT4 GPTQ quantized LoRA-tuned model.
Sample battery: 500+ corpus (M3 target).

| Metric | Target |
|---|---|
| Primary 3-category F1 mean | ≥ 0.82 |
| Macro F1 | ≥ 0.75 |
| FPR on benign | < 5 % |
| Latency p50 (SMS short input, ≤ 100 Korean chars) | < 300 ms optimization, < 500 ms M2 gate |
| Model file size | < 1.5 GB after INT4 |
| Peak RAM during inference | < 2 GB |

Intermediate verification — Mi:dm 2.0 Mini CPU smoke test on MacBook
(pre-M2): run `scripts/benchmark_mi_dm.py`. Expected laptop CPU latency
is several seconds per sample (no acceleration), which verifies model
loading and correctness, not production latency.

## Layer 3 Metacognition Probe

### Planned — Brier score baseline (M4, 2026-09)

Pilot at 성남시 어르신복지관 measures per-user Brier score over a
3-month window. No baseline measurement yet; hypothesis is tested in M4.

| Metric | Target |
|---|---|
| Mean Brier score (pilot cohort) | < 0.25 (below random baseline) |
| Brier score trend over 12 weeks | decreasing |
| Relationship anomaly detection rate on curated romance/investment cases | ≥ 60 % |

## End-to-end pipeline

### Planned — Full SMS path on Galaxy S24 (M3, 2026-08)

| Stage | Target latency |
|---|---|
| Layer 1 SMS ingest → normalized event | < 10 ms |
| Layer 2 Mi:dm inference (short input) | < 300 ms |
| Layer 3 probe evaluation | < 50 ms |
| Layer 4 Soft overlay render | < 100 ms |
| **End-to-end (incoming SMS to warning)** | **< 500 ms** |

## Cost and Carbon

Informational only, reported from M2 onward:
- NIPA GPU hours consumed per training run.
- Wall-clock minutes for full LoRA pipeline.
- Estimated cloud API cost per 1k classifications.

---

## Change log

- 2026-04-21 added Solar-pro baseline v0.2 expanded battery
- 2026-04-20 added Solar-pro baseline v0.1 initial measurement
- 2026-04-18 document created
