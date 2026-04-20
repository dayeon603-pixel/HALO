# HALO Architecture Decision Records (ADRs)

Design decisions with their context, rationale, alternatives, and
consequences. Format adapted from Michael Nygard's ADR template.

Each ADR is immutable once accepted. Supersession is marked by a new
ADR rather than editing an old one.

---

## ADR-001: On-device inference for Layer 2

**Status:** Accepted (2026-04-18)

**Context.** HALO processes sensitive communications (SMS, voice in
Phase 2). Korean 통신비밀보호법 Article 3 and 개인정보보호법 impose
strict constraints on transmission of message content. A cloud-based
classifier would be faster to prototype but would require transmitting
raw text off-device.

**Decision.** All Layer 2 classification runs on-device using ONNX
Runtime Mobile with Qualcomm QNN or Samsung NNAPI acceleration.

**Alternatives considered.**
1. Pure cloud classification with encrypted payloads. Rejected: still
   requires raw content transmission which is legally ambiguous.
2. On-device rule-based classifier with cloud fallback for hard cases.
   Rejected: the hard cases are precisely the generative scams where
   cloud inference is needed, creating a privacy regression.
3. Federated learning with on-device training. Deferred to Phase 3.

**Consequences.**
- Positive: clear legal compliance, minimal server trust surface,
  offline-capable.
- Negative: constrained to small models (under 3B params with
  quantization) for latency, requires per-device model deployment,
  limits real-time context expansion.
- Drives ADR-002 (model choice) and ADR-003 (four-layer design).

---

## ADR-002: KT Mi:dm 2.0 Mini (2.3B) as primary classifier

**Status:** Accepted (2026-04-18), supersedes initial Solar-mini choice

**Context.** Layer 2 needs a Korean-native LLM that fits on-device in
INT4 within roughly 2GB RAM and meets 국내 AI 연계 트랙 vendor list
(KT, LG AI연구원, NC AI, SKT, Upstage).

**Decision.** KT Mi:dm 2.0 Mini (2.3B parameters), published on
HuggingFace as `K-intelligence/Midm-2.0-Base-Instruct`. Primary
on-device classifier. Upstage Solar-pro used as cloud helper for
long-form analysis and auto-generated reports.

**Alternatives considered.**
1. Upstage Solar-mini. Rejected: 10.7B parameters does not fit on
   mobile for target p50 latency.
2. LG EXAONE-small. Deferred: no clean 2B-class checkpoint released at
   decision time.
3. Non-Korean small models (Llama 3.2 1B, Qwen 2.5). Rejected: fails
   국내 AI 연계 트랙 requirement; Korean language quality uncertain
   without fine-tuning.

**Consequences.**
- Positive: real public checkpoint, 2.3B fits with INT4, satisfies
  100 percent domestic rule, strong Korean fluency.
- Negative: smaller than ideal for complex reasoning (mitigated by
  LoRA + domain-specific fine-tuning), license review (Modified MIT)
  required before broad redistribution.

---

## ADR-003: Four-layer architecture

**Status:** Accepted (2026-04-18)

**Context.** Scam defense requires input collection, classification,
calibration, and intervention. Mixing these into a single component
creates coupling that blocks later phase extensions.

**Decision.** Adopt a four-layer separation:
- Layer 1 Sensing: raw input collection per channel.
- Layer 2 Classification: Korean sLLM inference per message.
- Layer 3 Metacognition Probe: user confidence and relationship tracking.
- Layer 4 Intervention: three-level escalation with user UI.

Each layer has a stable interface so that implementations can be swapped
(e.g., cloud vs on-device classifier, different LoRA adapter per
language) without breaking other layers.

**Alternatives considered.**
1. Monolithic pipeline. Rejected: impossible to test layers
   independently, hard to Phase-2 extend.
2. Three-layer (merge Probe with Intervention). Rejected: the probe's
   state is orthogonal to intervention decisions; separation clarifies
   evaluation.

**Consequences.**
- Clean test boundaries (see `tests/test_schema.py`, `test_risk_engine.py`).
- Easy swap of Layer 2 implementations (cloud prototype, on-device
  production, future language-specific adapters).
- Minor overhead in defining inter-layer schemas.

---

## ADR-004: Three-level intervention escalation

**Status:** Accepted (2026-04-18)

**Context.** A single threshold for "warn vs act" is too blunt.
Warnings that are too loud burn trust; hard blocks that are too
aggressive break legitimate user actions.

**Decision.** Three intervention levels: SOFT (warning), MEDIUM (family
alert + video call), HARD (5-minute transfer lock + family second
factor). Thresholds tuned from pilot data.

**Alternatives considered.**
1. Binary (block or pass). Rejected: legal concerns about blocking
   without clear criteria.
2. Pure warning (SOFT only) forever. Rejected: addresses only low-risk
   cases, misses high-risk financial transfer moments.

**Consequences.**
- Preserves user self-determination while enabling protective escalation.
- Requires family onboarding UX (Phase 2).
- Threshold tuning is a research question, not a fixed design.

---

## ADR-005: Y1 scope is SOFT only

**Status:** Accepted (2026-04-18)

**Context.** Solo founder with 780 engineering hours over 6 months.
Full three-level intervention plus family web plus iOS would require
roughly 1,500 hours.

**Decision.** Y1 implements SOFT only, SMS channel only. MEDIUM and
HARD require family Companion Web and WebRTC infrastructure that is
deferred to Phase 2. Voice channel and messenger channel also deferred
pending legal counsel.

**Alternatives considered.**
1. Attempt full scope. Rejected: unrealistic solo budget, would sacrifice
   quality everywhere.
2. Skip pilot to fit more features. Rejected: pilot is the key evidence
   for proposal claims.

**Consequences.**
- Competition submission is narrow but rigorously tested.
- Phase 2 is well-defined and ready to execute post-competition.
- SOFT alone cannot prevent all scams but provides measurable value.

---

## ADR-006: Compete in 국내 AI 연계 트랙

**Status:** Accepted (2026-04-18)

**Context.** Competition has two tracks: 일반 (no model restriction) and
국내 AI (must use vendors KT, LG AI연구원, NC AI, SKT, Upstage). Same
prize pool. 국내 AI likely has fewer applicants and higher policy
alignment.

**Decision.** Submit under 국내 AI 연계 트랙. Use Mi:dm 2.0 Mini and
Solar-pro as the core stack.

**Alternatives considered.**
1. 일반 트랙. Rejected: our architecture is already 100 percent
   domestic; switching tracks gives up competitive advantage of smaller
   pool and policy alignment.
2. Apply to both. Rejected: forbidden by 제8조 ⑨.

**Consequences.**
- Positive: smaller competition pool, policy tailwind, natural alignment.
- Downside: safety net from 제17조 ⑤ means worst case is demotion to
  일반 (not disqualification).

---

## ADR-007: Apache License 2.0

**Status:** Accepted (2026-04-19)

**Context.** Open-source licensing signals maturity for AI research
projects. Competition 운영규정 제21조 ② restricts external disclosure,
requiring clarification.

**Decision.** Apache License 2.0. Permissive, includes patent grant,
standard for AI/ML projects. 대회 공개 관련 제21조 ②는 주관기관과 사전
협의되었거나 협의 예정임을 명시.

**Alternatives considered.**
1. All Rights Reserved during competition, decide later. Rejected:
   judges cannot inspect code transparently; signals less confidence.
2. MIT. Rejected: lacks patent grant protection.
3. Custom license. Rejected: friction for contributors and reviewers.

**Consequences.**
- Full transparency for competition evaluation.
- Contributors accept Apache 2.0 CLA implicitly.
- Post-competition consultation with 주관기관 can refine if needed.

---

## ADR-008: Pilot at 성남시 어르신복지관

**Status:** Accepted tentative, pending 공문 회신 (2026-04-18)

**Context.** Pilot requires 5~10 elderly participants in a low-friction
setting. Team lead holds elected position as 성남시 청소년의회 의장,
providing legitimate network access to 성남시 복지 시설.

**Decision.** 성남시 어르신복지관 as primary pilot site. Formal
cooperation letter (공문) submitted through the city welfare department
in M1.

**Alternatives considered.**
1. Multiple cities from day one. Rejected: too much coordination
   overhead for solo founder.
2. Online-only recruitment. Rejected: elderly users need hands-on
   onboarding.

**Consequences.**
- Dependency on city cooperation response.
- Backup plan: adjacent 지자체 (인천, 수원) 복지관.
- IRB approval (공용IRB) must precede any participant contact.

---

## ADR-009: Ephemeral buffer privacy model

**Status:** Accepted (2026-04-18)

**Context.** Raw message content must be analyzed but not persisted
long-term on device or on server.

**Decision.** Raw input (SMS text, voice buffer, screen capture) lives
in device memory ephemeral buffer for at most 30 seconds, then is
cleared. Only derived metadata (category, risk score, hashed sender
identifier) persists in encrypted SQLite. Server receives only
aggregated opt-in telemetry.

**Alternatives considered.**
1. Encrypted local persistence of raw content. Rejected: still exposes
   content during decryption, violates minimization principle.
2. No local storage at all. Rejected: loses audit capability that
   users request (in-app event history).

**Consequences.**
- Strong legal posture under 개인정보보호법 and 통신비밀보호법.
- Audit log is forensic metadata, not raw content.
- Debugging in production requires reproducing with synthetic data.

---

## ADR-010: Language-agnostic Layer 2 with LoRA adapter swap

**Status:** Accepted (2026-04-18)

**Context.** Global expansion to Japan, English markets, and beyond
requires language-specific classifiers. Building separate codebases per
language is expensive.

**Decision.** Layer 2 core interface is language-agnostic. Each market
is served by a LoRA adapter trained on language-specific scam corpus,
loaded into the appropriate base model (Mi:dm for Korean, NTT Tsuzumi
for Japanese, Llama 3.2 for English).

**Alternatives considered.**
1. Single multilingual model. Rejected: quality gap vs specialized
   per-language models; Korean model would pay for parameters unused
   at inference in other languages.
2. Separate native apps per market. Rejected: maintenance burden.

**Consequences.**
- Single codebase supports multiple markets.
- Each market needs its own corpus, evaluation, and legal review.
- Phase 2 priority: Japanese LoRA before English.

---

## Template for new ADRs

```
## ADR-NNN: Title

**Status:** Proposed | Accepted (YYYY-MM-DD) | Superseded by ADR-XXX

**Context.** Background facts and forces shaping the decision.

**Decision.** The selected approach.

**Alternatives considered.** Options rejected and why.

**Consequences.** Positive, negative, and neutral follow-on effects.
```
