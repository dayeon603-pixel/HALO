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

### Baseline v0 (Solar-pro cloud, 2026-04-20, n=25 demo battery)

Cloud prototype baseline produced by `halo.demo.classifier_demo` against the
25-sample demo battery (`src/halo/demo/classifier_demo.py` SAMPLE_MESSAGES,
including 4 SPS-style adversarial variants). Raw outputs at
`experiments/baseline_v0_solar_pro/{report.md, results.json}`.

**Headline:** primary 3-category F1 mean **0.869** (target ≥ 0.82, **clears**);
adversarial robustness **4/4 = 100%**; macro-F1 0.880; overall accuracy 88%.

| Category | P | R | F1 | n |
|---|---|---|---|---|
| voice_phishing | 1.00 | 0.60 | 0.75 | 5 |
| romance_scam | 1.00 | 0.67 | 0.80 | 3 |
| investment_scam | 0.80 | 1.00 | 0.89 | 4 |
| loan_scam | 1.00 | 1.00 | 1.00 | 2 |
| subsidy_scam | 0.75 | 1.00 | 0.86 | 3 |
| family_impersonation | 0.75 | 1.00 | 0.86 | 3 |
| benign | 1.00 | 1.00 | 1.00 | 5 |
| **macro** | **0.90** | **0.89** | **0.88** | **25** |

Latency (Upstage Solar-pro API, cloud, ms): min 674, avg 994, p50 899, p95 1418, max 1519.

**Errors (3 of 25, all base samples, none adversarial):**
1. voice_phishing → family_impersonation. "어머님, 아드님이 교통사고로 중환자실..."
   uses a family-impersonation surface pattern while being a voice-phishing script.
2. voice_phishing → subsidy_scam. "국세청 체납 담당..." triggers a subsidy prior
   because of 국세청. Discriminator: urgency to transfer vs refund.
3. romance_scam → investment_scam. "미국 유전 엔지니어... 한국 투자 파트너."
   One-sentence romance scripts that pivot to investment are genuinely ambiguous.

Interpretation: all three errors are hybrid-category cases where one scam type
uses another's surface pattern. This motivates Layer 3 (metacognition probe,
relationship-anomaly tracking) rather than purely surface-level Layer 2 classification.
LoRA fine-tuning on 300+ corpus targets these boundary cases explicitly. A
secondary run with `solar-mini` (2026-04-20, same battery) produced identical
F1 0.869 but higher latency (p50 1392 ms), so `solar-pro` is retained as the
cloud-side reference.

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
