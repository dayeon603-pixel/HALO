# HALO
**H**olistic **A**gent for **L**ocal-inference **O**bservation

> 어르신 옆에서 "잠깐만요"를 대신 말해주는 온디바이스 한국어 sLLM 사기 방어 에이전트.
> A real-time, on-device Korean sLLM scam-defense agent for elder users.

[![CI](https://github.com/dayeon603-pixel/HALO/actions/workflows/ci.yml/badge.svg)](https://github.com/dayeon603-pixel/HALO/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status: Pre-alpha](https://img.shields.io/badge/Status-Pre--alpha-orange)]()
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)]()
[![Built with Mi:dm 2.0 Mini](https://img.shields.io/badge/sLLM-KT_Midm_2.0_Mini-green)]()
[![2026 AI Champion](https://img.shields.io/badge/2026-AI_Champion_%EB%8C%80%ED%9A%8C-red)]()

---

## 한눈에

| 항목 | 내용 |
|---|---|
| **문제** | 한국 2024년 보이스피싱 피해 **8,545억 원** (경찰청, 역대 최고). 60세 이상 피해 금액 비중 약 35~40%. |
| **해결** | 5채널(SMS·통화·카톡·화면·URL)을 온디바이스 Korean sLLM이 실시간 분석, 3단계 가족 연결형 개입 |
| **핵심 연구 자산** | [MetaMirage](https://www.kaggle.com/competitions) 메타인지 부호 역전 발견 (r = −0.84), Kaggle AGI Benchmark Challenge 2026 제출 |
| **타겟 플랫폼** | Android (주력), iOS (Phase 2) |
| **트랙** | 2026 AI Champion 대회 — 국내 AI 연계 트랙 |
| **팀대표** | 강다연 (Dayeon Kang) |

---

## 왜 HALO인가

기존 보이스피싱 방어 체계는 세 가지 구조적 실패를 공유한다.

1. **블랙리스트 지연** — 신종 수법이 등재되기까지 평균 수일~수주. 그 사이 피해 확산.
2. **단일 채널 분절** — 최신 사기는 카톡 접촉 → 통화 신뢰 구축 → SMS 링크 → 금융앱 이체의 **4+ 채널 연결 시나리오**이지만 기존 솔루션은 각 채널을 독립 처리.
3. **사용자 확신 공백** — 피해자는 이체 순간까지 "나는 안 속고 있다"고 확신한다. 기존 솔루션은 이 **메타인지 실패**를 측정하지 않는다.

HALO는 세 가지를 동시에 해결한다.

1. **생성형 대응** — 온디바이스 Korean sLLM이 블랙리스트 없이 처음 보는 스크립트를 분류한다.
2. **5채널 통합 분석** — SMS, 통화(Whisper-ko STT), 카톡(AccessibilityService), 금융앱 화면(OCR), URL(Safe Browsing).
3. **메타인지 이중 신호** — 본 팀의 MetaMirage 연구를 인간 사용자 확신도 추적에 전이. `Risk = α·PatternScore + β·UserConfidence + γ·RelationshipAnomaly`.

---

## 시스템 구조 (4-Layer)

```
Layer 1  SENSING         →  5채널 수집 (SMS·통화·카톡·화면·URL)
Layer 2  CLASSIFICATION  →  KT Mi:dm 2.0 Mini (2.3B) 온디바이스, 6+1 카테고리 분류
Layer 3  METACOG PROBE   →  사용자 확신도 · 관계 누적 추적 (MetaMirage 전이)
Layer 4  INTERVENTION    →  Soft / Medium(가족 연결) / Hard(이체 잠금)
```

자세한 아키텍처는 [`docs/architecture.md`](docs/architecture.md) 참조.

---

## 리포지토리 구조

```
halo/
├── README.md                   # 본 문서
├── LICENSE                     # Apache-2.0
├── CLAUDE.md                   # AI-assisted dev 가이드 (세션 간 영속 컨텍스트)
├── pyproject.toml              # Python 툴체인 (Python 3.11+)
│
├── docs/                       # 🔷 전체 기술 문서
│   ├── whitepaper.md           # 상세 기술 백서 (제안서 확장판)
│   ├── architecture.md         # 4-Layer 시스템 설계
│   ├── privacy.md              # 통비법·개보법 준수 설계
│   ├── metacognition.md        # MetaMirage 전이 방법론
│   ├── scam_taxonomy.md        # 6 카테고리 분류 체계 + 실례
│   ├── evaluation.md           # 평가 프로토콜 · 벤치마크
│   └── roadmap.md              # 6개월 마일스톤 · Phase Gate
│
├── configs/                    # Hydra/YAML 설정
│   ├── base.yaml
│   ├── model_midm_mini.yaml
│   └── eval.yaml
│
├── data/
│   ├── raw/                    # 수집 원본 (never touch after download)
│   ├── processed/              # 재현 가능한 파이프라인 산출
│   └── features/               # 피처 스토어 출력
│
├── src/halo/                   # 🐍 Python 백엔드·ML 코어
│   ├── corpus/                 # Korean scam corpus 구축
│   │   ├── collectors.py       # 경찰청·금감원·커뮤니티 수집
│   │   ├── adversarial.py      # SPS 기반 적대 변형 생성
│   │   └── schema.py           # Pandera 데이터 스키마
│   ├── models/
│   │   ├── classifier.py       # 6 카테고리 sLLM 분류기
│   │   ├── probe.py            # 메타인지 프로브
│   │   └── risk.py             # Risk 스코어링 엔진
│   ├── training/
│   │   ├── lora_finetune.py    # Mi:dm 2.0 Mini LoRA 파이프라인
│   │   ├── evaluate.py         # 평가 하네스
│   │   └── delta_update.py     # 주간 델타 업데이트
│   ├── inference/
│   │   ├── onnx_export.py      # 모바일 배포용 ONNX 변환
│   │   └── quantize.py         # INT8/INT4 양자화
│   └── serving/
│       ├── family_api.py       # FastAPI 가족 Companion 백엔드
│       └── report_gen.py       # 경찰청 자동 신고 생성
│
├── android/                    # 🤖 Android 네이티브 앱 (Kotlin)
│   └── app/src/main/kotlin/com/halo/
│       ├── services/           # SMS / Accessibility / Call / Screen
│       ├── ml/                 # sLLM · Whisper · OCR 온디바이스
│       ├── risk/               # Risk Engine · Metacog Probe
│       ├── intervention/       # Soft · Medium · Hard
│       └── ui/                 # Jetpack Compose 화면
│
├── family_web/                 # 🌐 가족 Companion Web (React)
│   └── src/{components,pages,lib}
│
├── tests/                      # pytest — edge cases
├── scripts/                    # CLI scripts (build_corpus, train, eval, export)
└── notebooks/                  # 탐색용만, production import 금지
```

---

## 빠른 시작

Make targets (see `Makefile`):
```bash
make dev         # dev 의존성 + pre-commit 훅 설치
make test        # pytest 실행
make lint        # ruff + black 검사
make demo        # Solar-pro 분류기 프로토타입 실행
```

### 환경 점검
```bash
python scripts/check_env.py
```

### 분류기 데모 (Upstage Solar-pro API 프로토타입)
```bash
export UPSTAGE_API_KEY=<your_key>
python -m halo.demo.classifier_demo
```

### 데이터 파이프라인 (M1 목표)
```bash
python scripts/build_corpus.py \
    --sources police,kisa,community \
    --output data/processed/corpus_v0.parquet
```

### 모델 학습 (M2 목표, NIPA GPU)
```bash
python scripts/train.py --config configs/model_midm_mini.yaml
```

### 평가 (M2 목표)
```bash
python scripts/evaluate.py --config configs/eval.yaml
```

### Android Alpha (M3 목표)
```bash
cd android && ./gradlew assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Docker (선택)
```bash
docker build -t halo:dev .
docker run --rm -it halo:dev make test
```

---

## 로드맵 (6개월)

| 월 | 마일스톤 |
|---|---|
| **M1 · 2026-06** | Scam corpus v0 (300+ 사례) + 메타인지 프로브 설계 |
| **M2 · 2026-07** | Mi:dm 2.0 Mini LoRA 모델 v0 + Galaxy S24 latency 실측 + 평가 파이프라인 |
| **M3 · 2026-08** | Android Alpha (SMS + 카톡 통합) + Risk Engine v0 |
| **M4 · 2026-09** | 음성 통합 + 성남시 어르신복지관 파일럿 |
| **M5 · 2026-10** | iOS 포팅 + 금융앱 연동 + Hard 개입 완성 |
| **M6 · 2026-11** | 통신사/지자체 MOU + 오픈소스 공개 + 정량 효과 백서 |

상세: [`docs/roadmap.md`](docs/roadmap.md)

---

## 개인정보·법 준수 설계 요약

1. **100% 온디바이스 추론** — 음성·메시지 원본의 서버 전송 절대 금지
2. **Ephemeral buffer** — 분석 직후 원본 메모리에서 즉시 폐기
3. **메타데이터만 집계** — 카테고리·위험도·타임스탬프만 (PII 제외)
4. **명시적 옵트인** — 설치 시 각 채널별 개별 동의
5. **가족 권한 분리** — 설정 권한은 지정 가족에게만

상세: [`docs/privacy.md`](docs/privacy.md)

---

## 연구 기반

| 자산 | 역할 | 상태 |
|---|---|---|
| **MetaMirage** | Layer 3 메타인지 프로브 이론 기반. r = −0.84 부호 역전 발견. | Kaggle AGI Benchmark Challenge 2026 제출 (2026-04-16) |
| **SPS Framework** | 적대적 변형 corpus 생성 방법론 | 본 팀 보유 |
| **QuantFlow** | 투자 사기 탐지용 금융상품 구조 분석 | 본 팀 보유 |

---

## 기여

- [CONTRIBUTING.md](CONTRIBUTING.md): 기여 절차, 개발 환경, 코드 스타일
- [SECURITY.md](SECURITY.md): 보안 취약점 신고
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): 커뮤니티 행동 강령
- [CHANGELOG.md](CHANGELOG.md): 변경 이력

---

## 라이선스

**Apache License 2.0** ([LICENSE](LICENSE)).
자유로운 연구·상업적 활용 허용, 특허 조항 포함.
2026 AI Champion 대회 운영규정 제21조 ② 관련 공개 여부는 주관기관과 사전
협의되었거나 협의 예정이며, 대회 종료 후 협의 결과에 따라 조정 가능합니다.

## 인용

```bibtex
@software{halo2026,
  author = {Kang, Dayeon},
  title = {HALO: Holistic Agent for Local-inference Observation},
  year = {2026},
  url = {https://github.com/dayeon603-pixel/HALO}
}
```

## 연락

- 팀대표: 강다연 (Dayeon Kang)
- Email: dayeon603@gmail.com
- GitHub: [dayeon603-pixel/HALO](https://github.com/dayeon603-pixel/HALO)

---

> _저는 제가 속았을 때, 누가 '잠깐 다시 봐요'라고 말해주길 바랐습니다._
> _HALO는 수백만 명의 어르신께 그 한 마디를 대신 전합니다._
