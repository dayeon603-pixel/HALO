# Evaluation Protocol

Measurement plan for the HALO system across model, pipeline, and pilot.
Results produced by this protocol become the scientific evidence base for
the competition, for research papers, and for policy submissions.

## Stage 1: Model-level evaluation (M2)

Target: KT Mi:dm 2.0 Mini fine-tuned with LoRA on 300+ Korean scam corpus.

Primary metrics:
- F1 per category.
- F1 macro-average.
- Precision and recall per category.
- Expected Calibration Error (ECE) of risk_score.
- False Positive Rate on benign test subset.

Secondary metrics:
- Latency p50 and p95 on reference hardware (Galaxy S24 with Snapdragon 8 Gen 3).
- Model file size after INT4 GPTQ quantization.
- Peak RAM during inference.

Targets for M2 phase gate:
| Metric | Target |
|---|---|
| F1 primary 3 categories (voice_phishing, family_impersonation, benign) | ≥ 0.82 |
| F1 macro average | ≥ 0.75 |
| ECE | ≤ 0.05 |
| FPR on benign | < 5% |
| Inference p50 (SMS short) | < 500 ms (initial), < 300 ms after optimization |
| Model file size | < 1.5 GB |

Evaluation data split:
- 70% train, 15% validation, 15% test.
- Stratified split to preserve per-category distribution.
- Temporal ordering when possible so that training precedes evaluation in time.
- Hard negative set: 50 messages that mimic scam surface patterns but are benign.

## Stage 2: Baseline comparisons

Four baselines for ablation:

1. Keyword rule classifier. BM25 + hand-authored pattern dictionary.
2. Mi:dm 2.0 Mini zero-shot with prompt engineering, no fine-tuning.
3. Solar-pro zero-shot via API.
4. HALO LoRA-tuned Mi:dm 2.0 Mini (proposed).

Ablations:
- With vs without SPS adversarial augmentation.
- LoRA rank 8 vs 16 vs 32.
- With vs without Layer 3 metacognition probe.
- Dataset size 150 vs 300 vs 500 samples.

## Stage 3: Pilot evaluation (M4~M6)

Target: 5~10 elder users at 성남시 어르신복지관.

Duration: 3 months (M4 start, M6 wrap-up).

IRB: 국가생명윤리정책원 공용IRB approval required prior to recruitment.

Protocol:
1. Informed consent with caregiver assistance where needed.
2. HALO Alpha installed and configured by researcher.
3. Passive data collection on classification events and user responses.
4. Weekly check-in call with participant or family.
5. Monthly in-person session to discuss UX and observed scams.

Measurements:

| Metric | Instrument | Target |
|---|---|---|
| Real-world F1 | Manual review of classified events | ≥ 0.80 on primary 3 categories |
| Soft intervention acceptance rate | Log of user responses to warnings | ≥ 60% engagement with warning details |
| Weekly retention | App-open events | ≥ 60% (pilot cohort with family onboarding assistance) |
| Brier score | Layer 3 probe responses | Decreasing over 12 weeks (learning effect) |
| Scam incidents | Participant or family self-report | 0 incidents target |

Ethics:
- Participants can withdraw at any time.
- All data is device-local and deleted on request.
- No compensation influences data collection (compensation may be offered for time).

## Stage 4: Open benchmarks

Halo-probe-suite release includes:
- 500+ labeled Korean scam messages across 6+1 categories.
- Adversarial perturbation toolkit.
- Evaluation scripts that reproduce all stage 1 and 2 results.
- Model checkpoints (subject to competition-period license constraints).

External use cases:
- Other Korean LLM researchers evaluating safety.
- Policy research on AI 기본법 고위험군 implementation.
- Academic courses in applied NLP safety.

## Research paper targets

- ACL 2027 or EMNLP 2027: methodology paper on MetaMirage transfer with pilot Brier evidence.
- NeurIPS 2027 Datasets and Benchmarks: corpus release.
- CHI 2027: HCI paper on intergenerational intervention protocols.

## Reporting standards

Every reported number carries:
- Exact dataset split description.
- Random seed used.
- Hardware and software versions.
- Confidence interval or standard deviation.
- Base rate or prevalence context.

No marketing-style absolute claims.
