# Contributing to HALO

HALO is an active research and engineering project submitted to the 2026
AI Champion 대회. Contributions are welcome. This document describes how
to get set up and what to expect.

## Scope boundaries during the competition period

The 2026 AI Champion 대회 runs through November 2026. During this period:

- External contributors are welcome to open issues and submit PRs for bug
  fixes, documentation improvements, or the Phase 2 roadmap items.
- Core algorithmic changes to Layer 2 and Layer 3 are reserved for the team
  lead until after competition conclusion, per 운영규정 제21조 ②.
- New features outside the Y1 Phase 1 scope are welcome to be proposed as
  issues; implementation is parked for Phase 2.

## Development environment

```bash
git clone git@github.com:dayeon603-pixel/HALO.git
cd HALO
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,docs]"
pre-commit install
pytest
```

For Android:
```bash
cd android
./gradlew assembleDebug
```

For Family Web (Phase 2):
```bash
cd family_web
npm install
npm run dev
```

## Code standards

- Python 3.11 plus, full type hints, pydantic v2 for configs.
- Formatting: black. Linting: ruff. Type checking: mypy strict.
- No print statements. Use loguru or Python logging.
- Tests for any behavioral change. Aim for edge cases, not only happy path.
- Docstrings explain the why, not the what.
- No em dash or en dash as sentence connector in docs.

## Commit style

Short first line (72 chars max), imperative mood, mixing Korean and English
is fine when that matches the subject matter.

Example commit messages:
```
Add Korean scam corpus schema with Pandera validation
Fix SmsReceiver crash on empty body
Drop duplicate paraphrases from adversarial augmentation
```

## Branch conventions

- main: always green, always installable.
- feat/xyz: feature branches off main.
- fix/xyz: bug fix branches.
- docs/xyz: documentation-only branches.

## Pull request process

1. Open a PR from your feature branch into main.
2. CI must pass (lint plus tests).
3. At least one reviewer signs off. During Y1 Phase 1, that reviewer is the
   team lead.
4. Squash merge preferred for small changes; rebase merge for larger.

## Research and data contributions

Korean scam corpus contributions are welcome. Required:
- PII scrubbed before submission.
- Source attribution in the row record.
- License clearance confirmed (public domain or explicit permission).
- Cohen's kappa consistency check passes on 10% sample against existing labels.

## Reporting vulnerabilities

See SECURITY.md.

## Contact

- Team lead: 강다연, dayeon603@gmail.com.
- GitHub Issues: https://github.com/dayeon603-pixel/HALO/issues.
