# HALO Technical Whitepaper

**H**olistic **A**gent for **L**ocal-inference **O**bservation
국내 sLLM 기반 온디바이스 실시간 사기 방어 에이전트

_Version 0.4 · 2026-04-18_
_Author: 강다연 (Dayeon Kang, 16, Team Lead)_
_Competition: 2026 인공지능 챔피언 대회 · 국내 AI 연계 트랙 · 과기정통부_
_Repository: github.com/dayeon603-pixel/HALO_
_License: Apache-2.0_

---

## 0. Executive Summary

대한민국의 디지털 사기는 국가적 재난 규모에 도달했다. 2024년 보이스피싱 피해액은 **8,545억 원**으로 역대 최고를 기록했고(경찰청), 60대 이상은 전체 피해자의 약 25%, 피해 금액의 35~40%를 차지한다. 투자·로맨스·대출 사기까지 포함하면 실제 규모는 **연 1조 원** 이상으로 추정된다. 기존 방어 체계는 블랙리스트 지연, 채널 분절, 사용자 확신 공백이라는 세 가지 구조적 실패를 공유한다.

HALO는 이 세 실패를 동시에 해결하는 **4-Layer 온디바이스 아키텍처**다. KT Mi:dm 2.0 Mini(2.3B)를 주력 온디바이스 sLLM으로, Upstage Solar-pro를 클라우드 보조로 활용하여 **국내 AI 연계 트랙 요건을 충족**한다. 핵심 차별점은 의료 진단·기상 예측 분야에서 확립된 **calibration 이론(Brier 1950, Dawid 1982)**을 모바일 사기 방어 UX에 이식한 Layer 3 설계다. 팀대표는 Google DeepMind × Kaggle AGI Benchmark Challenge 2026에 제출한 LLM 메타인지 연구 **MetaMirage**(2026-04-16 제출) 배경을 가지며, 이 경험이 Layer 3 프로브 설계의 design inspiration으로 적용된다.

Y1(대회 6개월) 범위는 SMS 채널 + Mi:dm LoRA 분류기 + Soft 개입 + 성남시 어르신복지관 파일럿(5~10명)으로 **솔로 학업 병행 주 30시간 기준 780시간 예산 내**에서 엄격히 scope 관리된다. 음성·메신저·화면 채널, Medium/Hard 개입, iOS, 일본어/영어 확장은 모두 Phase 2로 이관한다. 본 백서는 이 결정의 근거, 검증 가능한 가설 구조, 그리고 5개년 확장 로드맵을 상술한다.

---

## 1. Problem Statement

### 1.1 국내 피해 규모 — 확정 통계

- **총 피해액(경찰청)**: 2024년 약 8,545억 원. 전년 대비 수직 상승. 2021년 종전 최고(7,744억)를 넘어 역대 최고.
- **건당 평균 피해액(경찰청)**: 2024년 약 **4,100만 원**. 2022~2023년 2,400만 원 대비 1.7배.
- **연령별 피해자 비중(경찰청 공공데이터포털)**: 60대 이상 피해자 수 약 25%, 피해 금액 비중 약 35~40%. 1인당 고액 피해 집중.
- **유형 분포**: 기관 사칭형(보이스피싱 고전형), 대출 사칭, 가족·지인 사칭, 지원금 사칭, 로맨스, 투자, 피싱 URL/SMS. 다채널 결합형 사기가 급증.

### 1.2 현대 한국 사기의 진화 패턴

2023~2024년 급증한 수법은 단일 채널이 아니라 **다채널 결합형**이다. 예시:

1. **접촉(카톡)**: "서울중앙지검 수사관입니다"
2. **신뢰 구축(전화)**: 사건 설명, 압박 · 협박
3. **링크 유도(SMS)**: 악성 URL 또는 앱 설치
4. **집행(금융앱 화면)**: 개별 이체 또는 악성앱을 통한 자동 이체

단일 채널 방어는 이 시나리오의 어느 한 단계만 보기 때문에 전체 패턴을 포착할 수 없다. 특히 로맨스 스캠·투자 사기는 **수일~수개월 단위의 관계 구축**을 통해 피해자 판단을 점진적으로 무너뜨리는데, 기존 솔루션은 단발성 이벤트만 검사한다.

### 1.3 기존 방어 체계의 3대 구조적 실패

**(a) 블랙리스트 지연.** 시티즌코난(경찰청·경찰대학 치안정책연구소·인피니그루 공동 개발)은 악성앱·번호 DB 기반. 신종 수법이 발견돼 DB 등재까지 **평균 수일~수주**. 그 사이 피해 확산. 2024년 추가된 실시간 AI 통화 분석은 개선점이나 여전히 단일 채널(통화)에 국한.

**(b) 채널 분절.** T전화·SKT 스팸필터링은 발신 번호 기반, AhnLab V3 Mobile은 앱·URL 시그니처 기반, KISA는 개별 수법 경보. 어느 누구도 **한 명의 사용자에게 일어나는 다채널 시나리오**를 통합 추적하지 않는다.

**(c) 사용자 확신 공백.** 기존 솔루션의 모든 개입은 "사용자 행동 변경"에 의존한다. 그러나 **피해자는 이체 순간까지 자신이 속고 있다는 사실을 인식하지 못한다.** 메타인지(자기확신에 대한 보정) 신호를 실시간 측정하지 않으면 개입 타이밍을 결정할 수 없다.

### 1.4 메타인지 공백 — 본질적 문제

본 팀장은 2025-11에 Twitter 암표 사기 피해를 당했다. 16세 디지털 네이티브이고 인터넷에서 자랐지만 **돈을 이체하는 순간까지 자신이 속고 있다는 신호를 감지하지 못했다**. 이는 "어르신은 스마트폰이 낯설어서, 젊은 사람은 멀쩡하다"는 이분법이 틀렸음을 보여주는 **보편적 메타인지 공백의 증거**다.

대한민국 60대 이상이 피해 금액의 35~40%를 차지하는 이유는 그들이 더 어리석거나 덜 조심해서가 아니다. 그들이 **더 고액의 금융 결정권**을 가졌고, **새로운 수법에 대한 노출 경험이 부족**하며, **가족과 실시간 크로스체크할 채널이 없어서**다. HALO는 이 세 조건을 기술로 보완하는 것을 목표로 한다.

---

## 2. Research Foundation

### 2.1 MetaMirage — 부호 역전 발견

본 팀장이 2026-04-16에 Google DeepMind × Kaggle AGI Benchmark Challenge 2026 Metacognition Track에 제출한 연구. **핵심 발견**: 대형 언어모델의 역량이 높아질수록 공학적으로 구성된 과제 집합에서의 **메타인지 정확도(자기확신과 실제 정답률의 일치도)가 오히려 낮아지는 부호 역전 현상**.

- **수치**: n = 7, r = −0.84, p ≈ 0.02, 95% CI: [−0.97, −0.31]
- **해석**: 이는 **예비적(preliminary) 결과**다. n = 7 소표본에서 CI가 매우 넓고, "인간 사용자로의 전이"는 전혀 다른 도메인이다. 본 연구의 방법론 구조를 응용하되, **전이 가설은 탐색적 가설로 명시**한다.
- **파일럿 검증 계획**: M4 성남시 복지관 파일럿에서 사용자 Brier Score 측정을 통해 "인간도 패턴 신호와 무관하게 과잉확신 구간이 존재하는가" 실증.
- **Fallback**: 전이 가설 불성립 시 Layer 3는 순수 베이지안 보정 엔진으로 퇴행 가능. 아키텍처 강건성 유지.

### 2.2 SPS Framework — 적대 변형 생성 방법론

본 팀의 Structured Perturbation Stability Framework는 트랜스포머 모델의 강건성을 측정하기 위해 **구조적 적대 변형**을 생성하는 방법론이다. HALO에서는 이를 **Korean scam corpus 확장**에 응용한다.

변형 유형:
- **이모지/공백 삽입**: `"서울중앙지✨검✨"`, `"계 좌 확 인"`
- **유사 도메인**: `gov24-bonus.kr`, `citizen-conan-official.com`
- **한자/영어 혼용**: `"Lg화학 한정"`, `"緊急"`
- **문맥 재배치**: 동일 의미, 다른 순서

이를 기본 corpus의 20% 비율로 추가하여 모델이 **문자열 매칭이 아닌 의미 기반 탐지**를 학습하도록 유도.

### 2.3 QuantFlow — 도메인 지식 전이

QuantFlow는 본 팀의 금융 시장 모델링 프로젝트(GARCH, HMM, Black-Scholes)로, 투자 사기 카테고리 탐지에서 **가짜 금융 상품의 구조적 비현실성**(예: 불가능한 수익률 보장, 비현실적 상한가 약속)을 판별하는 지식 기반을 제공한다.

### 2.4 인간 사용자 전이 가설 — 방법론 이식

MetaMirage에서 검증한 self-confidence probe 프로토콜을 모바일 UI로 이식:

1. 위험 징후 감지 시 사용자에게 강제 질문: *"이 사람을 얼마나 믿으세요? (1~10)"*
2. 응답 기록 + 과거 동일 맥락(발신자 카테고리)에서의 실제 결과 매칭
3. 사용자 Brier Score(예측-실제 간 제곱 오차) 계산
4. 개별 사용자의 **메타인지 편향 프로파일** 생성 — 어떤 상황에서 과잉확신 경향이 있는지 학습
5. 상대방별 신뢰도 시계열로 관계 누적 추적 (장기 사기 포착)

---

## 3. System Architecture

### 3.1 설계 원칙 (5개)

1. **Privacy by Default**. 원본 미디어(음성·SMS·메신저·화면)는 기기 내 ephemeral buffer에만 존재. 서버 전송 금지.
2. **On-device First**. Layer 2 추론은 기기 내. Solar-pro 클라우드는 보조(장문 분석·신고 양식 자동 생성)로만 활용.
3. **Family-Connected Escalation**. 단독 차단이 아니라 가족 연결(Phase 2). 자기결정권 존중 + 긴급 개입의 법적 균형.
4. **Research-Backed**. 모든 설계 결정은 citation 또는 측정 가능 가설로 추적. "느낌" 기반 엔지니어링 금지.
5. **100% Domestic AI**. 국내 AI 연계 트랙 요건. Mi:dm 2.0 Mini(KT) + Solar-pro(Upstage).

### 3.2 4-Layer 개요

```
┌────────────────────────────────────────────────────────┐
│ Layer 1: SENSING — 5채널 입력 수집                      │
│   Y1: SMS + URL/QR                                     │
│   Phase 2: 음성 · 메신저 · 금융앱 화면                   │
└───────────────────┬────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────────────┐
│ Layer 2: CLASSIFICATION — Korean sLLM (LoRA-tunable)    │
│   주력 온디바이스: KT Mi:dm 2.0 Mini 2.3B INT4 (on QNN) │
│   클라우드 보조: Upstage Solar-pro (장문 / 가족 Web)    │
└───────────────────┬────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────────────┐
│ Layer 3: CALIBRATION PROBE — Brier Score 기반          │
│   사용자 확신도 + 관계 누적 시계열 + Brier Score         │
│   Risk = α·Pattern + β·Confidence + γ·RelationshipAnom │
└───────────────────┬────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────────────────┐
│ Layer 4: INTERVENTION — 단계적 개입                     │
│   Y1: Soft (경고)                                       │
│   Phase 2: Medium (가족 영상통화) · Hard (이체 잠금)     │
│   POST: 경찰청 신고 양식 자동 생성                       │
└────────────────────────────────────────────────────────┘
```

### 3.3 Layer 1 — SENSING (채널 상세)

| 채널 | Y1 구현 | Phase 2 | 주요 API | 법적 주의 |
|---|---|---|---|---|
| SMS/MMS | ✓ | — | `BroadcastReceiver`, `READ_SMS` | 개보법 동의 |
| URL/QR | ✓ | — | ML Kit Barcode + Safe Browsing | 공개 정보 |
| 음성 통화 | ✗ | ✓ | `AudioRecord` + 온디바이스 Whisper | **통비법 제3조 회색지대** |
| 메신저 (카톡) | ✗ | ✓ | `AccessibilityService` | **Play Store 심사 엄격** |
| 금융앱 화면 | ✗ | ✓ | `MediaProjection` + ML Kit OCR | 민감정보 처리 |

Y1에 SMS·URL만 포함한 이유는 법적·정책적 리스크가 가장 낮고, 단독 구현 가능 범위에 부합하기 때문.

### 3.4 Layer 2 — CLASSIFICATION

**주력 모델**: KT Mi:dm 2.0 Mini (2.3B 파라미터)
- HuggingFace: `K-intelligence/Midm-2.0-Base-Instruct`
- 라이선스: Modified MIT (상업 이용 제한 검토 필요)
- 한국어 네이티브 학습
- INT4 GPTQ 양자화 후 디스크 약 1.2GB, RAM 약 1.5GB
- Qualcomm QNN (Snapdragon 8 Gen 3+) / Samsung NNAPI 가속 대상

**클라우드 보조**: Upstage Solar-pro
- 장문 통화 녹취 분석, 가족 Companion Web 백엔드, 경찰청 신고 양식 자동 생성
- 국내 AI 연계 트랙 요건 추가 충족(Upstage는 지정 5개사 중 1)

**입출력 스키마**:
```json
{
  "category": "voice_phishing|romance_scam|investment_scam|loan_scam|subsidy_scam|family_impersonation|benign",
  "risk_score": 0-100,
  "rationale": "한국어 판단 근거 1-2문장",
  "key_signals": ["신호1", "신호2", "신호3"]
}
```

**훈련**: LoRA (rank 16, α 32, lr 1e-4, 3 epoch), bitsandbytes 4bit, A100 GPU (NIPA 지원 요청).

**평가**: 6+1 카테고리 F1 개별 측정. 주요 3 카테고리(보이스피싱·정상·가족사칭) 목표 F1 ≥ 0.82. 로맨스·투자 F1 0.70~0.80 예상 (의미 중첩 때문). 전체 평균 ≥ 0.75.

### 3.5 Layer 3 — CALIBRATION PROBE

**동작 순서**:
1. Layer 2 Risk 점수 ≥ θ_probe일 때 Layer 3 활성화
2. 사용자에게 모바일 UI로 강제 질문: *"이 사람(발신자)을 얼마나 믿으세요? (1~10)"*
3. 응답 저장 + 발신자·카테고리별 프로파일 업데이트
4. 과거 **동일 맥락(발신자 ID + 카테고리)**에서의 실제 결과(피해/정상) 대조
5. Brier Score 계산: `BS = mean((predicted_confidence - actual_outcome)^2)`
6. BS가 높으면(편향 강함) 개입 임계값 낮춤 (민감하게 개입)

**상대방별 신뢰도 시계열**:
- 특정 발신자와의 상호작용마다 신뢰도 업데이트
- 급격한 신뢰 상승 구간(의심 신호 후 신뢰 상승)을 **이상 탐지**로 포착
- 로맨스·투자 사기의 장기 조작 패턴에 특히 유효

**Risk 통합 공식**:
```
Risk = α · PatternScore (Layer 2 output)
     + β · UserOverconfidence (1 - Brier Score)
     + γ · RelationshipAnomaly (derivative of trust time series)
```
α, β, γ는 파일럿 데이터로 튜닝. 초기 가중치: α=0.5, β=0.3, γ=0.2.

### 3.6 Layer 4 — INTERVENTION

**Y1 — SOFT 개입만 구현**:
- 전체화면 경고 오버레이 (화면 자동 덮기)
- "잠깐만요, 다시 확인해 주세요" + 근거 3문장 (Layer 2 rationale)
- 유사 사기 사례 안내 (KISA 공개 경보 인용)
- 사용자는 "확인했어요 / 계속 / 가족에게 알릴게요" 선택

**Phase 2 — MEDIUM/HARD**:
- MEDIUM: 지정 가족에게 자동 푸시(FCM) + 즉시 영상통화(WebRTC) 연결
- HARD: 금융앱 이체 버튼 5분 잠금 + 가족 2차 비밀번호 요구 (금융앱 API 연동 선행 필요)

**POST (Y1 포함)**:
- 경찰청 사이버수사대 신고 양식 자동 생성 (PDF/HWP)
- 증거: 메시지 타임라인, Layer 2 판단 근거, URL 증거
- Solar-pro API로 양식 포맷팅

### 3.7 Data Flow & Privacy Boundaries

```
[사용자 기기 내부]                          [서버]
┌────────────────────────────────┐  │
│ SMS 수신                        │  │
│   ↓                             │  │
│ Ephemeral Buffer (30초 TTL)     │  │  ← 원본 절대 전송 금지
│   ↓                             │  │
│ Mi:dm on-device 추론             │  │
│   ↓                             │  │
│ Risk Score + Category (메타데이터만) │─────→ 집계 통계 (PII 제외)
│   ↓                             │  │
│ Layer 3 사용자 프로브            │  │
│   ↓                             │  │
│ Layer 4 Soft 개입               │  │
│   ↓                             │  │
│ (Phase 2) 가족 알림 트리거       │─────→ 암호화 FCM 푸시
└────────────────────────────────┘  │
                                    │
                          Solar-pro 클라우드 API
                          (사용자가 "가족에게 알림"
                           선택 시에만 비식별 요약 전송)
```

---

## 4. Technical Specifications

### 4.1 모델 선정 — 왜 Mi:dm 2.0 Mini

| 모델 | 파라미터 | 온디바이스 가능 | 국내 AI 트랙 | 공개성 |
|---|---|---|---|---|
| **KT Mi:dm 2.0 Mini** | **2.3B** | **✓ (INT4 1.2GB)** | **✓** | **HuggingFace 공개** |
| Upstage Solar-mini | 10.7B | ✗ (너무 큼) | ✓ | API only |
| Upstage Solar-pro | 22B+ | ✗ | ✓ | API only |
| LG EXAONE | 다양 | 일부 가능 | ✓ | 일부 공개 |
| NC VARCO | 다양 | 제한적 | ✓ | 제한적 |

Mi:dm 2.0 Mini는 **유일하게 모바일 온디바이스 가능 + 국내 AI + 공개 가중치** 조합을 만족한다.

### 4.2 양자화 — GPTQ INT4

Mi:dm 2.0 Mini (2.3B params, FP16 기준 4.6GB) → GPTQ 4bit INT4 → **1.2GB 디스크**, **1.5GB RAM**. 대형 Android 기기(8GB+ RAM) 배포 가능.

### 4.3 하드웨어 대상

| 등급 | 예시 기기 | 지원 |
|---|---|---|
| **Tier 1** (주력) | Galaxy S24+, S25 시리즈, Z Fold6+ | Snapdragon 8 Gen 3/4 QNN, 12GB+ RAM |
| Tier 2 | Galaxy S22+, A55 | Snapdragon 8 Gen 1 / Exynos, 8GB+ |
| Tier 3 (제한) | 구형 모델 | 메모리 제약, 성능 저하 감수 |

### 4.4 지연 예산 (p50 기준 목표)

| 단계 | Y1 목표 | Phase 2 목표 |
|---|---|---|
| SMS 수신 → Layer 1 정규화 | < 10ms | < 10ms |
| Layer 2 Mi:dm 추론 (단문) | < 300ms | < 200ms |
| Layer 3 프로브 (사용자 대기 제외) | < 50ms | < 50ms |
| Layer 4 Soft 개입 렌더링 | < 100ms | < 100ms |
| **End-to-end (단문)** | **< 450ms** | **< 350ms** |

**초기 실측 계획**: M2 종료 시 Galaxy S24 기기에서 Mi:dm 2.0 Mini INT4 ONNX Runtime Mobile 기준 Layer 2 p50 measurement. 예상치가 아닌 실측치 공개.

### 4.5 메모리 풋프린트

| 컴포넌트 | RAM (활성) | 디스크 |
|---|---|---|
| Mi:dm 2.0 Mini INT4 | 1.5GB | 1.2GB |
| Whisper-small INT8 (Phase 2) | 500MB | 300MB |
| Android 앱 전체 | < 3GB (Tier 1), < 2GB (Tier 2) | < 2GB |

---

## 5. Korean Scam Corpus

### 5.1 데이터 소스

- **경찰청 보도자료 및 공공데이터포털**: 연도별·유형별·연령별 통계 + 대표 수법 사례
- **KISA 인터넷침해대응센터 공개 경보**: 신종 수법 주간 공표
- **금감원 보이스피싱 실태조사 보고서**: 연 1회
- **커뮤니티 공개 피해 게시글**: 네이트판, 디시인사이드, 클리앙 등 공개 스레드 (개인정보 제거 후)
- **자체 합성**: 보이스피싱 녹취 공개 자료 + 위 수법 패턴으로 SPS 기반 변형

### 5.2 6+1 카테고리 정의

| 카테고리 | 정의 | 대표 키워드 | 예시 수 |
|---|---|---|---|
| voice_phishing | 공공기관·금융기관 사칭, 수사 협조 유도 | 서울중앙지검, 검사, 수사관, 계좌 동결 | 50+ |
| romance_scam | 관계 구축 기반 금전 요구 | 해외 파견, 투자, 결혼 이야기 | 40+ |
| investment_scam | 고수익 보장, 내부자 정보 | 상한가, 코인 상장, 내부 추천 | 50+ |
| loan_scam | 저금리 특별 대출 | 신용 회복, 저금리, 당일 승인 | 40+ |
| subsidy_scam | 정부 지원금·환급 사칭 | 근로장려금, 환급, 정부24 링크 | 40+ |
| family_impersonation | 자녀·손주 위장 긴급 송금 | 엄마 나야, 폰 고장, 급해서 | 40+ |
| benign | 사기가 아닌 일반 메시지 | — | 50+ |
| **합계 (초기)** | | | **310+** |
| **M3 확장 목표** | | | **500+** |

### 5.3 적대 변형 생성 (SPS 방법론)

원본 샘플 → 변형 함수 → 적대 샘플 (20% 비율)

```python
def perturb(text: str, method: str) -> str:
    if method == "emoji_spacing":
        # 서울중앙지검 → 서울중앙지✨검✨
        ...
    elif method == "similar_domain":
        # gov.kr → gov24-bonus.kr
        ...
    elif method == "char_mixing":
        # LG → Lg, 한자 혼용
        ...
    elif method == "context_reorder":
        # 문장 순서 재배치
        ...
```

### 5.4 라벨링 프로토콜

1. **1차 라벨링**: 팀장이 카테고리 + 주요 근거 키워드 3개 라벨링
2. **2차 검증**: 대한노인학회 또는 KISA 자문 패널의 10% 샘플 재검증
3. **라벨링 일관성 지표**: Cohen's κ ≥ 0.75 유지
4. **이견 샘플**: 제거 또는 "애매" 플래그로 별도 보관

### 5.5 프라이버시 친화 큐레이션

- 모든 커뮤니티 게시글에서 **이름·전화번호·계좌번호·주소·고유 식별자** 제거 (정규표현식 + 수동 검토)
- 공개 도메인(경찰청·KISA) 자료 우선
- IRB 사전 자료 승인 후에만 실 피해자 데이터 수집 (M4)
- 라이선스: 수집 단계에서 재배포 가능 여부 각 건별 기록

---

## 6. Training Methodology

### 6.1 LoRA 파인튜닝

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=16,                    # rank
    lora_alpha=32,           # scaling
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(base_mi_dm, config)
# trainable params: ~18M (vs 2.3B full model)
```

**Hyperparameters**:
- learning rate: 1e-4 (cosine decay, warmup 10%)
- batch size: 4 (effective 16 with grad accumulation)
- epochs: 3
- max sequence length: 512 tokens
- seed: 42 (reproducibility)
- mixed precision: bf16

### 6.2 Cross-validation

- 5-fold stratified CV on 300+ corpus
- Per-fold F1, precision, recall
- Category-level breakdown (especially for minority classes)

### 6.3 Delta Update Pipeline

주간 리셋:
```
경찰청·KISA 공개 feed 수집 → 신규 수법 샘플 10-20건 추가
→ LoRA 어댑터만 추가 미세조정 (1 epoch)
→ ONNX 변환 + INT4 양자화
→ 10MB 어댑터 파일만 배포 (OTA)
```

사용자는 전체 2.3B 모델을 재다운로드할 필요 없음. 어댑터만 10MB 업데이트.

---

## 7. Evaluation Protocol

### 7.1 Metrics

| 지표 | 측정 대상 | 목표 |
|---|---|---|
| **F1 (per category)** | Layer 2 분류 | 주요 3 ≥ 0.82, 평균 ≥ 0.75 |
| **Precision / Recall** | Layer 2 | 균형 test set 기준 |
| **ECE** (Expected Calibration Error) | Layer 2 confidence | ≤ 0.05 |
| **오탐률 (FPR)** | Layer 2 on benign | < 5% (균형 test set) |
| **Brier Score** | Layer 3 사용자 프로브 | < 0.25 (낮을수록 보정 good) |
| **End-to-end latency p50/p95** | 전체 pipeline | < 450ms / < 900ms |
| **파일럿 D7 유지율** | 앱 사용 유지 | ≥ 60% (파일럿 코호트) |

### 7.2 Benchmarks

- **Baseline 1**: 키워드 규칙 기반 분류기 (BM25 + 사전)
- **Baseline 2**: Mi:dm 2.0 Mini zero-shot (LoRA 없음)
- **Baseline 3**: Solar-pro zero-shot (API)
- **HALO v1**: Mi:dm 2.0 Mini + LoRA (본 제안)

Ablation:
- With/without SPS adversarial augmentation
- LoRA rank 8 vs 16 vs 32
- With/without Layer 3 metacognition probe

### 7.3 Pilot Human Study (M4-M6)

- 대상: 5~10명 어르신 (성남시 복지관)
- 기간: 3개월
- 측정:
  1. Layer 2 분류 정확도 (실 수신 메시지 기준)
  2. Soft 개입 수용률 (사용자가 "확인" vs "무시" 선택)
  3. 주간 유지율 (앱 실행 여부)
  4. Layer 3 사용자 Brier Score (메타인지 편향 프로파일)
  5. 실 피해 사건 발생 여부 (0건 목표)

**IRB**: 공용IRB(국가생명윤리정책원) 사전 심사 승인 필수. 취약 계층 대상 연구임을 명시, 참여자 사전 동의서, 언제든 중단 권리, 데이터 폐기 보장.

---

## 8. Intervention Design

### 8.1 3단계 에스컬레이션

| 단계 | 트리거 Risk | 동작 | Y1 구현 |
|---|---|---|---|
| **SOFT** | Risk ≥ 50 | 전체화면 경고 + 근거 + "계속/중단" 버튼 | ✓ |
| **MEDIUM** | Risk ≥ 75 | 가족에게 푸시 + 영상통화 연결 | Phase 2 |
| **HARD** | Risk ≥ 90 (금융앱 이체 대기 중) | 이체 5분 잠금 + 가족 2차 비밀번호 | Phase 2 |

임계값은 파일럿에서 튜닝. 초기값은 규칙에 의한 것이고 실 사용자 데이터로 조정.

### 8.2 Family Connection Protocol (Phase 2)

- 사전 설정: 어르신 계정에 1~3명의 가족 구성원 등록
- 인증: OAuth + 가족 관계 증빙 (선택)
- 알림 경로: FCM(Android) / APNs(iOS)
- 영상통화: WebRTC + TURN 서버 (Coturn)
- 암호화: E2E (libsodium)

### 8.3 UX for 어르신

- 기본 텍스트 크기 Apple-grade Dynamic Type XXL
- 색상 대비 WCAG AAA
- 음성 안내 (Korean TTS)
- 3-tap 이내 주요 동작 완료
- "자녀가 설정 → 어르신은 '확인' 버튼만" 원칙
- 실패 UX 테스트: 성남시 복지관 파일럿 실시

### 8.4 Legal Framework

- **자기결정권**: 최종 이체 결정은 사용자 본인. HALO는 정보 제공 + 연결 보조.
- **가족 개입 권한**: 어르신 사전 동의 기반. 동의 철회 즉시 가족 알림 중단.
- **법무법인 자문 진행**: 통신비밀보호법 제3조(대화 당사자 아닌 감청) 및 금융소비자보호법 관련. 2026년 M3 완료 목표.

---

## 9. Privacy and Compliance

### 9.1 Threat Model

- **외부 공격자**: 원본 음성/메시지 유출 → 통신비밀 침해. 대응: 서버 전송 금지.
- **내부 공격자(앱 개발자)**: 임의 로깅. 대응: 오픈소스 + 코드 감사.
- **사기범**: HALO 우회 시도. 대응: 주간 델타 업데이트 + 커뮤니티 기반 신종 수법 수집.
- **정부·감독기관**: 합법적 요청 시 대응 범위. 대응: 메타데이터만 저장, PII 없음.

### 9.2 통신비밀보호법 (제3조)

통신의 비밀과 자유를 침해하지 않으려면 **당사자 동의 + 기기 내 처리 + 원본 비전송**이 핵심. 문자(SMS)는 수신자 본인 동의로 처리 가능. 음성 통화는 양방 당사자 동의가 원칙이어서 **Phase 2 법무 자문 완료 후 재검토**.

### 9.3 개인정보보호법

- **수집 최소화**: 메시지 분석 시 카테고리와 Risk만 저장. 원문은 폐기.
- **정보주체 동의**: 설치 시 명시적 옵트인. 철회 언제든 가능.
- **민감정보**: 없음 (HALO는 건강·종교·정치 정보 수집 안 함).
- **위탁**: Upstage Solar-pro API 사용은 "위탁 처리" 공지 필요.

### 9.4 Audit Trail

- 모든 Layer 2 판단: 해시된 입력 + 카테고리 + 점수 (PII 제외)
- 저장 위치: 기기 내 암호화 SQLite
- 보존 기간: 90일 (이후 자동 삭제)
- 사용자 조회권: 언제든 앱 내에서 조회·다운로드·삭제

### 9.5 공용IRB 연구윤리

- 사전 신청: 국가생명윤리정책원 공용IRB
- 문서: 연구계획서, 동의서, 개인정보처리방침, 리스크 관리 계획
- 예상 심사 기간: 2~4개월 → M1에 신청, M4 승인 후 파일럿 개시

---

## 10. Roadmap

### 10.1 Y1 (대회 6개월 · 2026-06 ~ 2026-11)

| 월 | 산출물 | 예산 (hr) |
|---|---|---|
| **M1** | Corpus v0 (300+), Mi:dm 환경, IRB 신청 | 130 |
| **M2** | LoRA v0 모델, S24 실측 benchmark | 130 |
| **M3** | Android MVP (SMS + Soft 개입) | 150 |
| **M4** | 성남시 파일럿 개시 (5~10명) | 130 |
| **M5** | 중간 데이터 수집·분석 | 130 |
| **M6** | 최종 분석, 오픈소스 공개, 대회 결선 | 110 |
| **합계** | | **780 hr** (주 30hr × 26주) |

### 10.2 Phase 2 (대회 이후)

- 메신저(카카오) 채널 (Play Store 정책 대응)
- 음성 통화 채널 (법무 자문 완료 후)
- 금융앱 화면 채널
- Medium/Hard 개입 (가족 Companion Web + 금융 API)
- iOS 포팅
- 일본어 LoRA 어댑터 (NTT Tsuzumi 기반)
- 영어 LoRA 어댑터 (Llama 3.2 1B 기반)

### 10.3 Phase Gates

- **M2 종료**: F1 ≥ 0.82, latency 실측 기록
- **M4 종료**: IRB 승인, 복지관 공문 확보, 파일럿 5명 이상 동의
- **M6 종료**: 파일럿 정량 데이터, 오픈소스 공개, 결선 발표 준비 완료

---

## 11. Impact Analysis

### 11.1 직접 경제 영향

- 60대 이상 피해 금액: 약 3,000억 (8,545 × 35~40%)
- 파일럿 목표 방어율: 30% (UK FCA 은행 차단 연구 근거)
- 연간 방지 가능 피해: 약 900억 (파일럿→전국 확산 시나리오)

### 11.2 연구·학계 영향

- **Korean Multi-channel Scam Probe Suite**: 한국어 LLM 안전성 평가 공공재
- **MetaMirage 전이 방법론**: LLM 메타인지 연구의 실사회 응용 최초 사례
- **논문**: ACL 2027, NeurIPS 2027 Datasets & Benchmarks, CHI 2027 목표

### 11.3 정책 영향

- **AI 기본법 (2026-01-22 시행) 고위험 AI 안전성 평가**: 실증 도구 제공
- **공용IRB 취약계층 연구 프로토콜**: 본 파일럿이 참조 사례화 가능

### 11.4 글로벌 확산

- **Phase 2 일본**: 특수사기 피해 717억엔(2024). NTT Tsuzumi 2 기반 일본어 어댑터. 수법 구조적 유사성이 전이 효율 담보.
- **Phase 3 영어권**: 미국 60+ 피해 $2.4B(FTC 2024). Llama 3.2 1B English LoRA. AARP·Which? 파트너십 협의 필요.
- **Phase 4 동남아·기타**: GASA 2023 글로벌 사기 $1조+ 시장. 현지 sLLM + LoRA.

---

## 12. Risks and Mitigations

| # | 리스크 | 완화 |
|---|---|---|
| R1 | Mi:dm 2.0 Mini 라이선스 상업 제한 | 라이선스 재검토 + Upstage Solar-pro 하이브리드로 전환 가능 |
| R2 | 통비법 음성 채널 불허 | Phase 2로 이관 (Y1 범위 외) |
| R3 | 카톡 AccessibilityService Play Store 반려 | Phase 2 이관, 카카오 SDK 협의 |
| R4 | 파일럿 IRB 지연 | M1 조기 신청, 백업: 자문 IRB 경로 |
| R5 | MetaMirage 전이 가설 실패 | 베이지안 보정 엔진으로 퇴행 (아키텍처 강건) |
| R6 | 성남시 복지관 협조 실패 | 인접 지자체(인천·수원) 백업, 청소년의회 소개장 활용 |
| R7 | Solo 시간 부족 | Scope 엄격 관리, M6 phase-gate로 중단 권한 |
| R8 | 오탐률 > 5% | 3단계 개입으로 오탐 피해 제한, Hard 전 가족 확인 |

---

## 13. Appendices

### Appendix A: 카테고리별 대표 스크립트

**voice_phishing 예시**:
> "서울중앙지방검찰청 김철수 검사입니다. 귀하의 계좌가 금융사기 사건에 연루되어 즉시 확인이 필요합니다."

**romance_scam 예시**:
> "해외 파견 근무 중인 미군 의사입니다. 시리아 임무 중 귀하의 따뜻한 메시지에 위로를 받고 있습니다."

**investment_scam 예시**:
> "【내부 정보】 LG화학 내일 상한가 90% 확실. 선입금 500만원 가능하신 분만 연락."

### Appendix B: Metacognition Probe 프로토콜

MetaMirage 논문 §3.2 방법론 차용. 모바일 UI 변환:

1. 트리거: Layer 2 Risk ≥ 50
2. 질문: "이 사람(발신자)을 얼마나 믿으세요? 1(전혀 아님) ~ 10(완전히)"
3. 응답 시간 측정 (빠른 응답 = 신뢰 or 무관심, 느린 응답 = 주저)
4. 저장: `{timestamp, sender_id, category, confidence, response_time, actual_outcome_TBD}`
5. 배치 분석: 주 1회, Brier Score 갱신

### Appendix C: API Specifications

**Layer 2 Classifier API** (서비스 인터페이스):
```python
def classify(text: str) -> ScamResult:
    """한국어 메시지 분류. Mi:dm on-device 또는 Solar-pro fallback."""
```

**Family Notification API** (Phase 2):
```typescript
POST /api/v1/notify
{
  "user_id": "uuid",
  "event_type": "medium_risk|hard_risk",
  "category": "voice_phishing",
  "risk_score": 0-100,
  "timestamp": "ISO-8601"
}
```

### Appendix D: 예시 평가 출력

```
Category                F1     Precision  Recall  Support
voice_phishing          0.89   0.91       0.87    50
family_impersonation    0.85   0.88       0.82    40
benign                  0.92   0.95       0.89    50
investment_scam         0.76   0.74       0.78    50
romance_scam            0.72   0.70       0.74    40
loan_scam               0.78   0.80       0.76    40
subsidy_scam            0.81   0.83       0.79    40
Macro Average           0.82   0.83       0.81
```

---

## References

1. 경찰청 공공데이터포털. "보이스피싱 연령별 피해 현황 2024." https://www.data.go.kr/data/15063815/fileData.do
2. 警察庁. "2024年特殊詐欺統計." https://www.npa.go.jp/bureau/criminal/souni/tokusyusagi/hurikomesagi_toukei2024.pdf
3. FTC. "Protecting Older Consumers 2024-2025." https://www.ftc.gov/system/files/ftc_gov/pdf/P144400-OlderAdultsReportDec2025.pdf
4. GASA. "Global State of Scams 2023." https://gasa.org
5. ITU. "Facts and Figures 2024." https://www.itu.int/itu-d/reports/statistics/2024/
6. 국가법령정보센터. "AI 기본법 (인공지능 산업 진흥 및 신뢰 기반 조성 등에 관한 기본법)." https://www.law.go.kr/lsInfoP.do?lsiSeq=268543
7. EU AI Act Annex III (고위험군 카테고리). https://artificialintelligenceact.eu/annex/3/
8. 시티즌코난 공식 사이트. https://citizen.quv.kr/
9. HuggingFace. "K-intelligence/Midm-2.0-Base-Instruct." https://huggingface.co/K-intelligence/Midm-2.0-Base-Instruct
10. Upstage. "Solar Mini Product Page." https://www.upstage.ai/products/solar-mini
11. 성남시청소년청년재단. https://snyouth.or.kr/
12. 공용기관생명윤리위원회. https://nibp.kr/xe/irb

---

_End of Whitepaper v0.4_
_Changelog: v0.4 (2026-04-18) — initial release with post-audit corrections_
