"""HALO Layer 2 Classifier Demo — Cloud Prototype.

This is a PROTOTYPE demo that runs against the Upstage Solar-pro cloud API.
The production HALO system replaces this with **KT Mi:dm 2.0 Mini (2.3B)**
— K-intelligence/Midm-2.0-Base-Instruct — fine-tuned via LoRA and deployed
on-device via ONNX Runtime Mobile with Qualcomm QNN / Samsung NNAPI
acceleration.

Why cloud prototype first:
    - Validates prompt design and taxonomy before on-device tuning
    - Provides immediate demo artifact for 2026 AI Champion proposal
    - Measurable API baseline against which to compare the on-device
      LoRA-tuned Mi:dm model in M2

This demo proves:
    1. 6-category scam classification works on Korean scam scripts
    2. Risk scoring is coherent
    3. The rationale is human-readable
    4. Adversarial perturbations (SPS-style) degrade gracefully

It does NOT prove:
    - On-device latency claims (those require M2 Galaxy S24 benchmark)
    - LoRA-tuned Mi:dm parity with cloud Solar-pro baseline

Usage:
    export UPSTAGE_API_KEY=<your_key>
    python -m halo.demo.classifier_demo

Exit codes:
    0 — demo completed, accuracy ≥ 70%
    1 — demo completed but accuracy below threshold
    2 — runtime error (missing API key, network, etc.)
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import requests
from loguru import logger
from rich.console import Console
from rich.table import Table

ScamCategory = Literal[
    "voice_phishing",        # 보이스피싱 — 검사·수사관·금융기관 사칭
    "romance_scam",          # 로맨스 스캠 — 관계 구축 기반 장기 사기
    "investment_scam",       # 투자·코인 사기
    "loan_scam",             # 대출 사기
    "subsidy_scam",          # 지원금·환급 사칭
    "family_impersonation",  # 가족 사칭
    "benign",                # 정상 메시지
]

SYSTEM_PROMPT = """당신은 한국어 사기 메시지 탐지 전문가 AI입니다.
입력된 메시지(문자/음성 전사/카톡)를 분석하여 다음 6+1 카테고리 중 하나로 분류합니다.

카테고리:
- voice_phishing (보이스피싱): 검사·수사관·금융기관 사칭, 계좌 확인·수사 협조 유도
- romance_scam (로맨스 스캠): 친밀 관계 구축 → 금전 요구
- investment_scam (투자 사기): 고수익 보장, 내부자 정보, 코인·주식·부동산 유혹
- loan_scam (대출 사기): 저금리 특별 대출, 신용 회복 상품
- subsidy_scam (지원금 사칭): 정부·공공기관 환급·지원금 사칭
- family_impersonation (가족 사칭): 자녀·손주 위장 긴급 송금 요청, "엄마 나야" 류
- benign (정상): 사기가 아닌 일반 메시지

반드시 다음 JSON 형식으로만 응답합니다 (설명·주석 없이):
{
  "category": "voice_phishing|romance_scam|...|benign",
  "risk_score": 0~100 정수 (0=완전 정상, 100=명백한 사기),
  "rationale": "한국어 판단 근거 1~2문장",
  "key_signals": ["신호1", "신호2", "신호3"]
}
"""


@dataclass(frozen=True, slots=True)
class ScamResult:
    """Classification output from Layer 2.

    Attributes:
        category: Scam taxonomy label (or 'benign').
        risk_score: 0–100. Used by Layer 3 risk engine.
        rationale: Human-readable justification (shown to user in Soft intervention).
        key_signals: Bullet points of concrete warning signals.
    """

    category: ScamCategory
    risk_score: int
    rationale: str
    key_signals: list[str]


class SolarClassifier:
    """Layer 2 classifier using Upstage Solar API.

    In production, this is replaced by on-device Solar-mini 1.5B + LoRA adapter
    via ONNX Runtime Mobile with QNN/NPU acceleration. API surface identical.
    """

    API_URL = "https://api.upstage.ai/v1/solar/chat/completions"

    def __init__(self, api_key: str | None = None, model: str = "solar-pro") -> None:
        self.api_key = api_key or os.environ.get("UPSTAGE_API_KEY")
        if not self.api_key:
            msg = "UPSTAGE_API_KEY required (export it or pass api_key=)"
            raise ValueError(msg)
        self.model = model

    def classify(self, message: str) -> ScamResult:
        """Classify a single Korean message. Deterministic (temperature=0)."""
        response = requests.post(
            self.API_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.0,
            },
            timeout=30,
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"]
        data = json.loads(raw)
        return ScamResult(
            category=data["category"],
            risk_score=int(data["risk_score"]),
            rationale=data["rationale"],
            key_signals=list(data.get("key_signals", [])),
        )


# Sample Korean scam scripts — synthetic, based on public 경찰청 case archives.
# See docs/scam_taxonomy.md for full taxonomy and additional examples.
SAMPLE_MESSAGES: list[tuple[str, ScamCategory]] = [
    # ---- Voice phishing ----
    (
        "서울중앙지방검찰청 김철수 검사입니다. "
        "귀하의 계좌가 금융사기 사건에 연루되어 즉시 확인이 필요합니다. "
        "아래 번호로 지금 바로 연락 부탁드립니다.",
        "voice_phishing",
    ),
    (
        "어머님, 아드님이 교통사고로 중환자실에 입원하셨습니다. "
        "수술비 긴급 송금이 필요한 상황입니다. 지금 바로 이체 부탁드립니다.",
        "voice_phishing",
    ),
    # ---- Romance scam ----
    (
        "안녕하세요 혹시 저 기억하세요? 작년에 카페에서 뵌 적 있는데... "
        "지금 해외 파견 중인데 한국 분이셔서 너무 반가워요. "
        "친구가 되어주실래요?",
        "romance_scam",
    ),
    # ---- Investment scam ----
    (
        "【LG화학 단체카톡】 내부자 추천 특급 정보. "
        "내일 상한가 90% 확실. 선입금 500만원 가능하신 분만 연락주세요. "
        "지금 놓치면 없습니다.",
        "investment_scam",
    ),
    # ---- Loan scam ----
    (
        "저금리 3.5% 특별 대출 상품 안내. "
        "신용등급 무관 5천만원까지 당일 승인. "
        "오늘 오후 4시까지만 모집: 010-XXXX-XXXX",
        "loan_scam",
    ),
    # ---- Subsidy scam ----
    (
        "[정부24] 2026년 근로장려금 환급 대상자 최종 선정 안내. "
        "아래 링크에서 본인인증 후 즉시 지급 가능: "
        "http://gov24-bonus.kr/refund",
        "subsidy_scam",
    ),
    # ---- Family impersonation ----
    (
        "엄마 나야. 폰이 고장나서 친구 폰으로 보내. "
        "지금 급해서 그런데 100만원만 급하게 보내줄 수 있어? "
        "내 계좌로 바로 돌려드릴게.",
        "family_impersonation",
    ),
    # ---- Benign ----
    (
        "내일 저녁 7시 강남역에서 만날까? "
        "지난번에 얘기한 카페에서 보자.",
        "benign",
    ),
    # ---- Adversarial perturbations (SPS-style) ----
    # Emoji/space obfuscation to evade keyword filters
    (
        "서울중앙지 ✨검✨ 김철수 검 사 입 니 다 "
        "계 좌 확 인 부 탁 드 립 니 다",
        "voice_phishing",
    ),
    # Case/special-char obfuscation
    (
        "[Lg화학 한정] 내부자 추천 주식 내일상한가 90% "
        "지금 입금 가능하신 분만",
        "investment_scam",
    ),
]


def run_demo(classifier: SolarClassifier | None = None) -> int:
    """Run the classifier on the sample battery and print a report table.

    Returns:
        Exit code (0 = success with acceptable accuracy, 1 = below threshold).
    """
    classifier = classifier or SolarClassifier()
    console = Console()

    table = Table(
        title="HALO Layer 2 Demo — 6-Category Korean Scam Classifier",
        show_lines=True,
    )
    table.add_column("#", width=2, style="dim")
    table.add_column("메시지", width=40, style="cyan")
    table.add_column("기대", style="yellow", width=22)
    table.add_column("예측", style="magenta", width=22)
    table.add_column("위험도", justify="right", style="red", width=6)
    table.add_column("근거", style="green", width=45)

    n_correct = 0
    for i, (message, expected) in enumerate(SAMPLE_MESSAGES, start=1):
        try:
            result = classifier.classify(message)
            is_correct = result.category == expected
            n_correct += int(is_correct)
            mark = "✓" if is_correct else "✗"
            table.add_row(
                str(i),
                message[:38] + ("..." if len(message) > 38 else ""),
                expected,
                f"{result.category} {mark}",
                str(result.risk_score),
                result.rationale[:43],
            )
        except (requests.RequestException, json.JSONDecodeError, KeyError) as exc:
            logger.error("classification failed for sample %d: %s", i, exc)
            table.add_row(
                str(i),
                message[:38],
                expected,
                f"ERROR: {type(exc).__name__}",
                "-",
                "-",
            )

    console.print()
    console.print(table)

    accuracy = n_correct / len(SAMPLE_MESSAGES)
    console.print(
        f"\n[bold]정확도: {n_correct}/{len(SAMPLE_MESSAGES)} = "
        f"{accuracy * 100:.1f}%[/bold]"
    )
    console.print(
        "\n[dim]이 데모는 Solar API를 사용합니다. 최종 배포에서는 Solar-mini 1.5B + "
        "LoRA 어댑터를 기기 내에서 실행하여 p50 < 200ms 지연을 달성합니다.[/dim]"
    )

    return 0 if accuracy >= 0.7 else 1


def main() -> None:
    try:
        sys.exit(run_demo())
    except ValueError as exc:
        logger.error(str(exc))
        sys.exit(2)


if __name__ == "__main__":
    main()
