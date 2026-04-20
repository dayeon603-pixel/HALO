# FAQ and Hostile Q&A Prep

Questions judges, reviewers, or skeptical engineers are likely to ask
HALO, with honest answers. This is the hostile Q&A rehearsal; prefer
reading this alongside `docs/whitepaper.md`.

---

## Competition and scope

### Why a solo high school student for a 5억 prize submission?

The proposal is grounded in published research (MetaMirage, Kaggle AGI
Benchmark Challenge 2026 Metacognition Track, submitted 2026-04-16) and
two prior team IP artifacts (SPS Framework, QuantFlow). The Y1 scope is
aggressively cut to 780 engineering hours (30 hr per week over 26 weeks)
with a single SMS channel and Soft-only intervention, which is feasible
for a motivated solo builder with advisory support. Phase 2 items
requiring co-development (voice, messenger, family web, iOS) are parked
until after the competition period.

### Why 국내 AI 연계 트랙, not 일반?

HALO's Layer 2 on-device model is KT Mi:dm 2.0 Mini (2.3B), which is on
the 연계 기업 list. Solar-pro is used as cloud helper, also on the list.
No foreign model is in the pipeline. The 국내 AI 트랙 has a smaller
applicant pool and stronger alignment with the government priority that
created the track. If 100 percent domestic compliance is challenged, per
제17조 ⑤ we are demoted to 일반 rather than disqualified, so the downside
is zero.

### Why 16세 founder authority concerns?

The founder is the first author of a Kaggle submission at the Google
DeepMind AGI Benchmark Challenge. The proposal's defensibility rests on
research credentials and rigorous scoping, not on age. All pilot work
will go through 공용IRB with proper caregiver consent procedures.

---

## Architecture and model

### Why KT Mi:dm 2.0 Mini, not Solar-mini or EXAONE?

Solar-mini is 10.7B parameters, which does not fit within the mobile NPU
memory budget for p50 sub-300ms inference. Mi:dm 2.0 Mini is 2.3B with
INT4 quantization fitting in 1.5GB RAM, and has publicly released
weights on HuggingFace under K-intelligence. LG EXAONE is split across
sizes without a clean mobile-deployable checkpoint at our target size.
NC VARCO is in a similar position. Mi:dm is the cleanest fit.

### Why on-device for Layer 2?

Privacy. Raw SMS and (Phase 2) voice must not leave the device per
통신비밀보호법 and 개인정보보호법. An on-device classifier processes
content in an ephemeral memory buffer and clears raw text within 30
seconds. Metadata-only server transmission is opt-in.

### Is p50 < 300ms realistic?

Initial benchmark expectation for Mi:dm 2.0 Mini 2.3B INT4 on Snapdragon
8 Gen 3 QNN with 256-token SMS input is 150 to 300 ms based on published
benchmarks for comparable 2B-class models. The proposal states p50 < 500
ms as the M2 gate, with < 300 ms as the optimization target. The M2
measurement replaces the estimate with a real number on Galaxy S24.

### Why not just use rule-based regex for scam detection?

Modern Korean scams evolve weekly, use emoji obfuscation, character
substitution, and contextual social engineering that bypass keyword
rules. The proposal shows 20 percent adversarial augmentation via SPS
Framework to demonstrate generative robustness. Rule baselines are
included in the evaluation plan as one of the ablations.

### How does MetaMirage (an LLM study) apply to humans?

It applies as a methodology transfer, not a proven fact. The probe
protocol (verbalized confidence, outcome resolution, Brier score) is
directly portable. Whether humans show the same sign-flip pattern is an
exploratory hypothesis tested in the M4 pilot. Layer 3 is designed to
fall back to plain Bayesian calibration if the transfer does not
replicate, so the architecture does not depend on the transfer holding.

---

## Data and research ethics

### Where does the corpus come from?

Three sources: public 경찰청 press releases and 공공데이터포털 statistics,
KISA 인터넷침해대응센터 advisories, and community posts (PII-scrubbed).
A fourth source is SPS-based adversarial perturbations of existing
samples. No raw user data is used in Y1 pre-pilot work. All pilot data
collection requires 공용IRB approval.

### What about the pilot with elderly subjects?

Pilot is small (5 to 10 participants) at 성남시 어르신복지관. It runs
after 공용IRB (국가생명윤리정책원) approval, with informed consent by the
participant and, where appropriate, family caregiver. Participants can
withdraw and have their data deleted at any time. Data is device-local
with 90-day retention and explicit opt-in for aggregated telemetry.

### Did you cherry-pick the 60세 이상 statistics?

No. The proposal reports both: 60세 이상 피해자 **수 비중 약 25 percent** and
**피해 금액 비중 약 35 to 40 percent**. Fewer victims, but higher per-person
loss because they hold more assets and have less recent exposure to
evolving attack patterns. Both numbers come from 경찰청 공공데이터포털
2024 연령별 통계.

---

## Legal compliance

### Is real-time voice call analysis legal under 통신비밀보호법?

It is a gray area. Article 3 prohibits interception without consent from
a party. The recipient of a call can consent to processing on their own
device, but the caller has not consented. This is why voice channel
is **Phase 2** in HALO, after completion of a law firm written opinion.
The Y1 scope includes only SMS, which has clearer consent grounding.

### What about KakaoTalk extraction via AccessibilityService?

Google Play restricts AccessibilityService use strictly. Apps that use
it for purposes outside disability assistance face heightened review,
and KakaoTalk's terms of service must be considered. This is why the
messenger channel is also **Phase 2**, after review of Play Store
policies and a potential alternative path via an official KakaoTalk SDK
partnership.

### Do you store any PII on the server?

No. Server-observable data is limited to: (1) anonymized category
distributions, (2) aggregated risk scores, (3) app health telemetry.
Sender identifiers are salted-hashed. Raw message content is never
transmitted. The only user-initiated cloud processing is opt-in
Solar-pro summarization of a user-requested 경찰청 신고 form.

---

## Economics and scale

### Why is Y2 ARR only 3~5억 won?

This is the conservative base case. Earlier drafts projected 33억 based
on aggressive 5 percent freemium conversion and 100 million installed
base assumptions that do not match Korean safety-app benchmarks. The
revised number uses 2 percent conversion on 30 million MAU and 1 to 2
small B2G PoC MOUs, which are defensible comparisons.

### Is 방어율 30 to 50 percent realistic?

The 30 percent pilot target is modeled on UK FCA bank-level call
friction studies showing 20 to 30 percent reduction in authorized push
payment fraud when friction is added. HALO's family-connected
escalation is expected to match or exceed that benchmark. The pilot
measures this directly, so the number is testable.

### Why no foreign markets in Y1?

Language-agnostic architecture is present (LoRA adapter swap per
language), but building a Japanese or English LoRA adapter requires
either a partnership or budget that does not exist in Y1. Phase 2
sequence is Japan (NTT Tsuzumi 2 base) then English (Llama 3.2 1B
base).

---

## Execution and team

### What happens if the solo founder is unavailable?

Phase gates at M2 and M4 provide formal go / no-go decision points. The
contingency is to either extend timelines via external contributor
recruitment or formally close out the project with the pilot report as
the primary deliverable. Source code and corpus are open for community
continuation.

### How is 성남시 어르신복지관 pilot access secured?

Through the team lead's 성남시 청소년의회 의장 position, formal
cooperation request is submitted to the city welfare department in M1.
This is not a guaranteed acceptance; if declined, alternative pilots at
adjacent 지자체 복지관 are pursued.

### What external advisors are engaged?

Advisory is planned in three areas: law firm for 통비법 analysis (M2),
대한노인학회 for research ethics (M1), and 경찰청 사이버수사국 for
real-world scam pattern verification (M1). None of these are formal
commitments yet; they are M1 outreach targets.

---

## Technical rigor

### Why Brier score specifically, not log loss or other calibration metrics?

Brier score is a proper scoring rule bounded on [0, 1] and interpretable
as the mean squared prediction error. It is commonly used in medical
and forecasting calibration studies, which makes cross-domain
comparison straightforward. Log loss is also valid but less
interpretable in a user-facing context.

### What prevents adversarial evasion of the classifier?

SPS-based adversarial augmentation at 20 percent of the training corpus
exposes the classifier to emoji injection, character substitution,
similar domain, and context reordering. Weekly LoRA adapter delta
updates close the gap on new patterns. A longer-term plan in Phase 2 is
to open a GitHub security disclosure channel for community-reported
bypasses.

### How do you handle concept drift?

The weekly delta update pipeline retrains the LoRA adapter on a rolling
window of the last 12 weeks of new patterns, with held-out evaluation
on a fixed benchmark set. Drift is measured as F1 degradation on the
fixed set; if drift exceeds 5 points, a full LoRA retrain is
scheduled.

---

## Miscellaneous

### What if this is just another 시티즌코난 clone?

시티즌코난 uses blacklist detection on one channel (phone calls) and has
added real-time AI analysis in 2024. HALO differs on four axes:
multichannel integration, generative classification without blacklists,
metacognition-aware intervention timing, and family-connected
escalation. The competitive analysis in proposal section 1.6 lays out
these differences with references.

### Is the project open source now or later?

Apache 2.0 license applies to the repository. Running code, reading code,
and inspecting the full design are permitted. Actual LoRA-tuned model
weights and trained classifier artifacts may be withheld during the
competition period per 운영규정 제21조 ② until organizer consultation
allows disclosure. The open-source release of the full pipeline
including trained weights is planned for M6 or just after.

### What is the most honest thing you can say about this submission's weaknesses?

Three real weaknesses: (1) the MetaMirage-to-human transfer is an
unproven hypothesis, (2) the solo execution window is tight even with
aggressive scoping, (3) external advisory relationships are targets not
commitments as of submission. Each is addressed in the proposal with an
explicit mitigation, but judges should weigh them accordingly.
