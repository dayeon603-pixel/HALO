# Security Policy

HALO handles sensitive communications on user devices. We take security
vulnerabilities seriously.

## Supported versions

During the 2026 AI Champion 대회 period, only the `main` branch is
supported. Post-competition, a tagged release policy will be adopted.

## Reporting a vulnerability

Please do not open a public GitHub Issue for security vulnerabilities.

Instead, email dayeon603@gmail.com with the subject line:
`[HALO Security] Brief description`.

Include:
- A clear description of the vulnerability.
- Steps to reproduce or a proof of concept.
- Your assessment of potential impact.
- Any suggested mitigation.

You can expect an acknowledgment within 48 hours and an initial status
update within 7 days.

## Disclosure timeline

We aim for coordinated disclosure. After the vulnerability is reproduced
and a fix is planned, we will agree on a public disclosure date, typically
within 90 days. Acknowledgment of the reporter is included unless
anonymity is requested.

## Scope

In scope:
- Android app binary and source code.
- Python backend components in `src/halo/`.
- Family Companion Web backend and frontend.
- Build pipelines and release artifacts.

Out of scope for this policy:
- Vendor vulnerabilities in upstream dependencies (PyTorch, ONNX Runtime,
  HuggingFace, KT Mi:dm, Upstage Solar). Report those to the respective
  vendors.
- Social engineering of the maintainer.
- Physical attacks on end-user devices.

## Responsible use

HALO is designed to protect users from scams. Using HALO code or derived
works to build scams, to extract user data without consent, or to evade
detection is prohibited and violates both the license and Korean law
(정보통신망법).
