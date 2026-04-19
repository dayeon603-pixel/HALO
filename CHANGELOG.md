# Changelog

All notable changes to HALO are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/) and this project adheres
to [Semantic Versioning](https://semver.org/) once it reaches v1.0.

## [Unreleased]

### Added
- Initial repository scaffold.
- Full whitepaper in `docs/whitepaper.md`.
- Six supporting docs: architecture, privacy, metacognition, scam taxonomy,
  evaluation, roadmap.
- Python package `src/halo/` with corpus, models, training, inference,
  and serving modules.
- Android Kotlin app skeleton targeting API 26 through 34.
- Family Companion Web skeleton with Vite plus React plus TypeScript.
- Classifier demo using Upstage Solar-pro API (cloud prototype).
- GitHub Actions CI for lint and tests.
- Pre-commit configuration.
- CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, NOTICE documents.
- Apache License 2.0.

### Planned for 0.2.0 (M2, 2026-07)
- KT Mi:dm 2.0 Mini LoRA fine-tuning pipeline complete.
- Evaluation harness with F1, ECE, and latency measurement.
- ONNX export and INT4 quantization.
- On-device latency benchmark on Galaxy S24.

### Planned for 0.3.0 (M3, 2026-08)
- Android Alpha build with SMS channel.
- Risk engine wired end to end.
- Corpus v1 with 500 plus samples.

### Planned for 1.0.0 (M6, 2026-11)
- Pilot completion at 성남시 어르신복지관.
- Open-source halo-probe-suite release.
- Research paper drafts for ACL 2027 and NeurIPS 2027.
