# CLAUDE.md — HALO Project

This file is the persistent project context for AI-assisted development sessions. Read this first.

## Project identity

**HALO** — Holistic Agent for Local-inference Observation
A real-time, on-device Korean sLLM scam-defense agent for elder users.
Competition: **2026 AI Champion 대회 · 국내 AI 연계 트랙** · 과기정통부 주최 · 2026-04-24 submission deadline

## Lead

- **팀대표:** 강다연 (Dayeon Kang), HS student, MetaMirage 제1저자, Structured Perturbation Stability Framework researcher, QuantFlow author
- **Email:** dayeon603@gmail.com
- **Role:** research lead, ML implementation, mobile development, partnership outreach

## Core research assets (team IP)

- **MetaMirage** — Kaggle AGI Benchmark Challenge 2026 submission (2026-04-16). Sign-flip finding: `r = −0.84 (n = 7)` between capability and metacognitive accuracy on engineered task families. **This is the foundation of Layer 3 (metacognition probe).**
- **SPS Framework** — Structured Perturbation Stability. Adversarial perturbation methodology for transformer robustness. Used to generate adversarial augmentation in the scam corpus.
- **QuantFlow** — Quant finance models (GARCH, HMM, Black-Scholes). Used for investment-scam pattern recognition.

## Architectural principles (enforce)

1. **Privacy by default.** Raw media (voice, SMS, messenger text) NEVER leaves the device. Server only sees metadata + aggregated stats.
2. **On-device first.** Inference target: Solar-mini 1.5B quantized + LoRA adapter, p50 latency < 200ms on Galaxy S23+.
3. **Family-connected escalation.** Never block alone. Always escalate through a designated family member at Medium/Hard.
4. **Research-backed.** Every design choice should trace to a citation or a measurable hypothesis. No vibes-only engineering.
5. **100% 국내 AI models** for core inference path — Upstage Solar-mini primary, KT Mi:dm-small backup. Required by competition track 국내 AI 연계.

## Stack

- **Python 3.11+**, full type hints, mypy compatible, black+ruff, loguru (no print)
- **Pydantic v2** for configs, dataclasses with `__slots__` for hot-path
- **PyTorch 2.3**, HuggingFace Transformers + PEFT(LoRA), bitsandbytes 4bit
- **ONNX Runtime Mobile** + Qualcomm QNN / Samsung NPU delegates
- **Android**: Kotlin 2.0, Jetpack Compose 1.7, Foreground Service, AccessibilityService
- **iOS** (Phase 2): Swift 5.10, SwiftUI, CallKit
- **Family Web**: React 18 + TypeScript + TailwindCSS + Vite, FastAPI backend

## Repository structure

See [README.md](README.md).

## What is locked vs. open

**Locked:**
- Name: HALO
- Tagline: "어르신 옆에서 '잠깐만요'를 대신 말해주는 AI"
- Track: 국내 AI 연계 트랙
- Architecture: 4-layer (Sensing → Classification → Metacognition → Intervention)
- Base model: Solar-mini 1.5B (primary)
- Scam taxonomy: 6 categories (보이스피싱, 로맨스, 투자, 대출, 지원금, 가족사칭)

**Open (decide as we go):**
- Team name on cover page — Dayeon pending
- High school name on cover page — Dayeon pending
- Co-applicant recruitment (depends on eligibility response from 과기정통부)
- Exact LoRA hyperparameters (to be tuned in M2)
- iOS technical details (Phase 2)
- Partnership specifics with 경찰청 sub-division, which telco, which 지자체 beyond 성남시

## Rules of engagement (Dayeon's preferences)

- Direct, no preamble. Recommendation > options.
- Code over prose for technical explanations.
- Advanced concepts OK; don't over-explain basics.
- Flag risks and edge cases proactively.
- Production-grade from day one — no "MVP hacks" left in code.
- Type everything. Test critical paths. Docstring the non-obvious.
- No `print()`. Use `loguru`.
- No hardcoded secrets. `.env` + pydantic-settings.
- Seeds set in every ML script.
- Temporal splits for any time-series data. Never random split.
- If a feature uses data not available at prediction time, mark `# LEAKAGE RISK:`.

## Important files

- [`docs/whitepaper.md`](docs/whitepaper.md) — extended technical proposal
- [`docs/architecture.md`](docs/architecture.md) — system design
- [`docs/privacy.md`](docs/privacy.md) — legal/privacy model
- [`docs/metacognition.md`](docs/metacognition.md) — MetaMirage transfer methodology
- [`docs/scam_taxonomy.md`](docs/scam_taxonomy.md) — 6-category definition + examples
- [`docs/evaluation.md`](docs/evaluation.md) — metrics, benchmarks, ablations
- [`docs/roadmap.md`](docs/roadmap.md) — 6-month Phase Gates

## Deadlines

- **2026-04-24 17:00 KST** — AI Champion 1차 제안서 제출 (internal target 2026-04-21)
- 2026-11 — expected finals (AI Festival)

## Competition rules (from 운영규정)

- 5-page max for 구현제안서 (excl. cover) — overflow auto-rejected
- Max 3 team memberships per individual (강다연 can be 팀장 on one, 팀원 on 2 others)
- 개발 결과물 외부 유출 금지 during competition period
- 동일/유사 개발 결과물 양 트랙 중복 금지
