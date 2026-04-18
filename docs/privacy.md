# Privacy and Legal Compliance

HALO handles sensitive communications. Every design choice in this document
reflects legal constraints under Korean law (통신비밀보호법, 개인정보보호법,
정보통신망법) and the principle of data minimization.

## Threat model

| Actor | Risk | Mitigation |
|---|---|---|
| External attacker | Raw voice or message exfiltration | Server transmission forbidden for raw media. |
| Malicious insider (app developer) | Unauthorized logging | Open source code, reproducible builds, audit log. |
| Scammer adapting to HALO | Model evasion | Weekly LoRA adapter delta updates. |
| Law enforcement lawful request | Subpoena of stored data | Device-local only; server holds metadata without PII. |

## 통신비밀보호법 (Protection of Communications Secrets Act)

Article 3 prohibits interception of communications without consent of a party.

Implications:
- SMS reception processed under Android `READ_SMS` with explicit user opt-in, treated as consent by the receiving party (the user).
- Messenger extraction (KakaoTalk via AccessibilityService, Phase 2) requires the same consent plus review of KakaoTalk's terms of service.
- Voice call real-time analysis is legally gray because the caller has not consented to analysis. This is why voice is Phase 2 after legal counsel.

HALO treats the user as the sole party whose consent grounds all processing.
Outbound notifications to family members are opt-in and revocable.

## 개인정보보호법 (Personal Information Protection Act)

Collection minimization:
- Classifications store `category` and `risk_score` plus a salted hash of the sender identifier. Original message text is not persisted after a 30-second ephemeral window.
- No health, religious, political, or biometric information is collected.

Consent:
- Opt-in at install for each channel (SMS, URL, voice later).
- Family member connection is a separate opt-in.
- Withdrawal available at any time in settings.

Processor disclosure:
- Upstage Solar-pro API use qualifies as "위탁 처리" (delegated processing).
  Users must be notified of processor identity and purpose.

User rights:
- Right to access: in-app view of stored audit log.
- Right to delete: in-app full-data wipe.
- Right to portability: export as JSON.

## 정보통신망법 (Information and Communications Network Act)

Relevant for malicious URL detection and notification features. Safe Browsing
calls use public APIs and do not transmit user PII.

## Audit trail

Stored device-locally (encrypted SQLite):
```
{
  "event_id": "uuid",
  "timestamp": "ISO-8601",
  "channel": "sms|url|voice|...",
  "sender_hash": "salted SHA-256",
  "category": "voice_phishing|...",
  "risk_score": 0,
  "action_taken": "soft_warning_shown|medium_alert|...",
  "user_response": "continued|stopped|family_notified"
}
```

Retention: 90 days, then automatic deletion. User can extend or shorten
per-app settings.

## 공용IRB (Institutional Review Board)

Pilot research (M4~M6) requires prior approval.

Target IRB: 국가생명윤리정책원 공용기관생명윤리위원회 (Public IRB at NIBP).

Submission package:
- Research protocol with clear primary and secondary endpoints.
- Informed consent form in accessible Korean.
- Data management plan (device-local, 90 day retention).
- Risk assessment including psychological risks of false-positive alerts.
- Advisory consultation letter from 대한노인학회.

Timeline: submission in M1, expected approval 2~4 months.

## Cross-border data transfer

None during Y1. Solar-pro API processing occurs on Upstage servers (Korea region).
If Phase 2 expands to Japan or English markets, new privacy assessments are
required before deployment.

## Vulnerabilities and disclosure

Contact: dayeon603@gmail.com for responsible disclosure.
Bug bounty: planned for post-release, not during competition period.

## Competition-period restrictions

Per 운영규정 제21조 ②, technical materials obtained during competition
participation are restricted from external disclosure without organizer
consultation. License terms for HALO will be finalized in consultation with
주관기관 (NIPA, TTA) following competition conclusion.
