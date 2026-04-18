# HALO System Architecture

Deep dive into the 4-layer on-device architecture. This document complements
`whitepaper.md` §3 with implementation-level detail for contributors.

## Design principles

1. Privacy by default. Raw media never leaves the device.
2. On-device first. Cloud only for auxiliary tasks (long-form summarization, family web backend).
3. Family-connected escalation. Not unilateral blocking.
4. Research-backed. Every design choice maps to a citation or a measurable hypothesis.
5. 100% domestic AI for Korean primary model (Mi:dm 2.0 Mini).

## Layer 1: Sensing

Android implementation.

| Channel | Y1 | API surface | Permission |
|---|---|---|---|
| SMS / MMS | ✓ | `BroadcastReceiver` + `SmsManager` | `READ_SMS` |
| URL / QR | ✓ | ML Kit Barcode + Safe Browsing | network only |
| Voice call | Phase 2 | `AudioRecord` + on-device Whisper | `RECORD_AUDIO` (통비법 자문 후) |
| Messenger (KakaoTalk) | Phase 2 | `AccessibilityService` | `BIND_ACCESSIBILITY_SERVICE` |
| Bank app screen | Phase 2 | `MediaProjection` + ML Kit OCR | `FOREGROUND_SERVICE_MEDIA_PROJECTION` |

Each channel produces a normalized `IncomingEvent` record with:

```kotlin
data class IncomingEvent(
    val id: UUID,
    val timestamp: Instant,
    val channel: Channel,
    val senderId: String?,      // hashed before persistence
    val text: String,           // raw content; ephemeral buffer only
    val metadata: Map<String, Any>,
)
```

Events flow through a Kotlin `Flow<IncomingEvent>` to Layer 2. Raw `text` is
cleared from memory within 30 seconds after classification completes.

## Layer 2: Classification

Core model: KT Mi:dm 2.0 Mini 2.3B (HuggingFace `K-intelligence/Midm-2.0-Base-Instruct`).

Deployment path:
1. Base model downloaded during app install (one-time, ~1.2 GB INT4).
2. LoRA adapter (~10 MB) shipped with app update or OTA delta.
3. ONNX export via Optimum with PEFT adapter merged.
4. Inference via ONNX Runtime Mobile 1.24.x with Qualcomm QNN delegate on
   Snapdragon devices, or Samsung NNAPI delegate on Exynos.

Auxiliary cloud model: Upstage Solar-pro (API) for long-form transcripts,
family-web backend summarization, and 경찰청 신고 양식 auto-generation.

Output schema (also defined in `src/halo/models/classifier.py`):

```json
{
  "category": "voice_phishing|romance_scam|investment_scam|loan_scam|subsidy_scam|family_impersonation|benign",
  "risk_score": 0,
  "rationale": "...",
  "key_signals": ["...", "..."]
}
```

Latency budget on Galaxy S24 / Snapdragon 8 Gen 3:
- SMS short input (< 100 Korean chars): p50 target 250ms, p95 500ms.
- M2 benchmark will replace these targets with measured values.

## Layer 3: Metacognition Probe

Trigger: Layer 2 `risk_score` crosses probe threshold (initial value 50).

User interaction:
1. Full-screen overlay with the message rationale (Layer 2 output).
2. Confidence probe: "이 사람을 얼마나 믿으세요? (1~10)"
3. User response recorded with response time.

State update:
```
history[sender_id].append({
    "timestamp": now,
    "category": classifier_category,
    "user_confidence": user_response,
    "response_time_ms": response_ms,
    "actual_outcome": None,  # filled in later if verifiable
})
```

Risk combination:
```
Risk = α · PatternScore (Layer 2)
     + β · UserOverconfidence (1 - Brier Score from history)
     + γ · RelationshipAnomaly (derivative of trust time series)
```

Initial weights: α=0.5, β=0.3, γ=0.2. Tuned on pilot data in M5.

Fallback path: if MetaMirage transfer hypothesis fails in M4 pilot (Brier
Scores do not differentiate future outcomes), Layer 3 reduces to a Bayesian
prior-update engine. Architecture remains robust to the hypothesis outcome.

## Layer 4: Intervention

Y1 implements SOFT only. Phase 2 adds MEDIUM and HARD.

| Level | Threshold | Action |
|---|---|---|
| SOFT | Risk ≥ 50 | Full-screen warning with rationale, user choices (continue / stop / notify family). |
| MEDIUM | Risk ≥ 75 | Auto-push to registered family members via FCM/APNs + WebRTC video call. |
| HARD | Risk ≥ 90 (during bank transfer) | 5-minute transfer lock + family second-factor password. |
| POST | After any positive detection | Auto-generate 경찰청 신고 양식 (PDF/HWP). |

Family connection (Phase 2):
- Pre-registration: user assigns 1~3 family members.
- Transport: FCM (Android), APNs (iOS), E2E encrypted via libsodium.
- Video call: WebRTC with Coturn TURN server.
- Consent model: user can revoke family linkage at any time.

## Data flow boundaries

Device memory only:
- Raw SMS content
- Voice audio buffers
- Screen captures
- Messenger extracts

Server-observable (metadata only, no PII):
- Anonymized category distribution
- Aggregate risk scores
- App health telemetry

Server-processed (opt-in, Solar-pro API):
- De-identified long-form transcripts for summarization
- 경찰청 신고 양식 draft generation (after user consent)

## Open questions for M1

- Exact Mi:dm 2.0 Mini license terms (Modified MIT clauses).
- Upstage Solar-pro rate limits and pricing for pilot.
- Qualcomm QNN SDK compatibility with Mi:dm architecture (first-party testing needed).
- Android `MediaProjection` behavior across OEM skins (Galaxy One UI vs stock).
