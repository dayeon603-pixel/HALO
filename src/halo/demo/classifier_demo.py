"""HALO Layer 2 Classifier Demo — Cloud Prototype.

This is a PROTOTYPE demo that runs against the Upstage Solar-pro cloud API.
The production HALO system replaces this with **KT Mi:dm 2.0 Mini (2.3B)**,
fine-tuned via LoRA and deployed on-device via ONNX Runtime Mobile with
Qualcomm QNN or Samsung NNAPI acceleration.

Why cloud prototype first:
    - Validates prompt design and taxonomy before on-device tuning.
    - Provides immediate demo artifact for the 2026 AI Champion proposal.
    - Establishes a measurable API baseline against which to compare the
      on-device LoRA-tuned Mi:dm model in M2.

This demo proves:
    1. 6+1 category classification works on realistic Korean scam scripts.
    2. Risk scoring is coherent.
    3. Rationale is human-readable.
    4. Adversarial perturbations (SPS-style) degrade gracefully.

It does NOT prove:
    - On-device latency claims (those require M2 Galaxy S24 benchmark).
    - LoRA-tuned Mi:dm parity with cloud Solar-pro baseline.

Usage:
    export UPSTAGE_API_KEY=<your_key>
    python -m halo.demo.classifier_demo [--samples path.json] [--report path.md]

Exit codes:
    0 — demo completed and primary-category F1 is at or above threshold.
    1 — demo completed but accuracy below threshold.
    2 — runtime error (missing API key, network, etc.).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import statistics
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import requests
from loguru import logger
from rich.console import Console
from rich.table import Table

ScamCategory = Literal[
    "voice_phishing",
    "romance_scam",
    "investment_scam",
    "loan_scam",
    "subsidy_scam",
    "family_impersonation",
    "benign",
]

PRIMARY_CATEGORIES: tuple[ScamCategory, ...] = (
    "voice_phishing",
    "family_impersonation",
    "benign",
)

SYSTEM_PROMPT = """당신은 한국어 사기 메시지 탐지 전문가 AI입니다.
입력된 메시지(문자/음성 전사/카톡)를 분석하여 다음 6+1 카테고리 중 하나로 분류합니다.

카테고리:
- voice_phishing (보이스피싱): 검사·수사관·금융기관 사칭, 계좌 확인·수사 협조 유도
- romance_scam (로맨스 스캠): 친밀 관계 구축 후 금전 요구
- investment_scam (투자 사기): 고수익 보장, 내부자 정보, 코인·주식·부동산 유혹
- loan_scam (대출 사기): 저금리 특별 대출, 신용 회복 상품
- subsidy_scam (지원금 사칭): 정부·공공기관 환급·지원금 사칭
- family_impersonation (가족 사칭): 자녀·손주 위장 긴급 송금 요청
- benign (정상): 사기가 아닌 일반 메시지

반드시 다음 JSON 형식으로만 응답합니다 (설명·주석 없이):
{
  "category": "voice_phishing|romance_scam|...|benign",
  "risk_score": 0~100 정수,
  "rationale": "한국어 판단 근거 1~2문장",
  "key_signals": ["신호1", "신호2", "신호3"]
}
"""


@dataclass(frozen=True, slots=True)
class ScamResult:
    """Classification output from Layer 2."""

    category: ScamCategory
    risk_score: int
    rationale: str
    key_signals: list[str]
    latency_ms: float = 0.0


class SolarClassifier:
    """Layer 2 classifier using Upstage Solar API.

    In production this is replaced by on-device Mi:dm 2.0 Mini + LoRA adapter
    via ONNX Runtime Mobile. API surface is identical.
    """

    API_URL = "https://api.upstage.ai/v1/solar/chat/completions"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "solar-pro",
        max_tokens: int | None = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("UPSTAGE_API_KEY")
        if not self.api_key:
            msg = "UPSTAGE_API_KEY required (export it or pass api_key=)"
            raise ValueError(msg)
        self.model = model
        self.max_tokens = max_tokens

    def classify(self, message: str) -> ScamResult:
        payload: dict[str, object] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.0,
        }
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens
        t0 = time.perf_counter()
        response = requests.post(
            self.API_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=30,
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"]
        data = json.loads(raw)
        return ScamResult(
            category=data["category"],
            risk_score=int(data["risk_score"]),
            rationale=data["rationale"],
            key_signals=list(data.get("key_signals", [])),
            latency_ms=latency_ms,
        )


# Expanded sample battery. 60 samples across 6+1 categories, including
# 17 adversarial SPS-style variants covering emoji spacing, character
# substitution, similar domains, multi-turn setups, hanja mixing,
# homoglyph attacks, and compressed/obfuscated forms.
# All samples are synthetic, based on public 경찰청 보도자료 case patterns.
SAMPLE_MESSAGES: list[tuple[str, ScamCategory, str]] = [
    # ========== voice_phishing (8 base + 4 adversarial) ==========
    ("서울중앙지방검찰청 김철수 검사입니다. 귀하의 계좌가 금융사기 사건에 연루되어 즉시 확인이 필요합니다.",
     "voice_phishing", "base"),
    ("어머님, 아드님이 교통사고로 중환자실에 입원하셨습니다. 수술비 긴급 송금이 필요한 상황입니다.",
     "voice_phishing", "base"),
    ("금융감독원 조사팀 박수사관입니다. 귀하의 명의로 불법 대출이 접수되었습니다. 지금 바로 조치가 필요합니다.",
     "voice_phishing", "base"),
    ("국세청 체납 담당입니다. 체납 세금 미납 시 자산 동결 처리됩니다. 즉시 확인 부탁드립니다.",
     "voice_phishing", "base"),
    ("대검찰청 사이버범죄수사단 이민수 수사관입니다. 귀하의 주민등록번호가 마약사건에 도용되어 긴급 보안계좌 이체가 필요합니다.",
     "voice_phishing", "base"),
    ("우리은행 보안팀 최영희 실장입니다. 귀하의 카드로 300만원 해외 승인이 시도되었습니다. 본인 확인 후 차단 처리해드리겠습니다.",
     "voice_phishing", "base"),
    ("경찰청 지능범죄수사대 강형사입니다. 귀하가 피해자로 등록된 사건이 있어 연락드렸습니다. 통화 녹음되니 솔직히 답해주세요.",
     "voice_phishing", "base"),
    ("건강보험공단 납부 조사과입니다. 장기요양보험 체납이 확인되었습니다. 오늘 중 납부하지 않으면 연체 가산금이 부과됩니다.",
     "voice_phishing", "base"),
    ("서울중앙지 ✨검✨ 김철수 검 사 입 니 다 계 좌 확 인 부 탁 드 립 니 다",
     "voice_phishing", "adversarial_emoji_spacing"),
    ("[긴급] 民事 소송 관련 출석 요청. 불응 시 압류 절차 진행. 확인: http://court-kr.co/notice",
     "voice_phishing", "adversarial_hanja_domain"),
    ("서울중앙지방검찰청입니다 . 귀하의. 계좌가. 사건에. 연루. 즉시연락.010-OOOO-XXXX",
     "voice_phishing", "adversarial_puncmangle"),
    ("검찰청ㅇ ㅣ민수 수사관ㅇ ㅣㅂ ㅁ다 긴급번ㅎ ㅗ OOOOXXXX",
     "voice_phishing", "adversarial_jamo_split"),
    # ========== romance_scam (6 base + 2 adversarial) ==========
    ("안녕하세요 혹시 저 기억하세요? 작년에 카페에서 뵌 적 있는데 지금 해외 파견 중인데 한국 분이셔서 너무 반가워요.",
     "romance_scam", "base"),
    ("시리아 임무 중인 미군 대위입니다. 고독한 시간에 당신의 메시지가 큰 위로가 됩니다. 특별한 관계가 되고 싶어요.",
     "romance_scam", "base"),
    ("미국 유전 엔지니어입니다. 한국 투자 파트너를 찾고 있어요. 믿을 수 있는 분이라 연락드립니다.",
     "romance_scam", "base"),
    ("서울에 방문 예정인데 당신에게 가방을 선물로 보냈어요. 관세 300달러만 대신 내주시면 도착해요. 배송번호 알려드릴게요.",
     "romance_scam", "base"),
    ("우리 만난 지 한 달 되었네요. 저 이번에 큰 프로젝트 투자 기회가 생겼어요. 당신 이름으로 같이 시작하면 수익 반반 나눠요.",
     "romance_scam", "base"),
    ("사실은 저 지금 공항에서 문제가 생겨서 500만원 필요해요. 당신이 믿을 사람이라 부탁드려요. 돌아가서 두 배로 갚을게요.",
     "romance_scam", "base"),
    ("안녕ㅎㅏ세요 혹시저 기 억 하세요 작 년카페 에서뵌적 있 는 데해외 파 견 중",
     "romance_scam", "adversarial_jamo_split"),
    ("Hello 저는 US army major 입니다. Syria 파견 중 ㅎㅏㄴ국분 만나 반갑네요.",
     "romance_scam", "adversarial_code_mix"),
    # ========== investment_scam (7 base + 3 adversarial) ==========
    ("【LG화학 단체카톡】 내부자 추천 특급 정보. 내일 상한가 90% 확실. 선입금 500만원 가능하신 분만 연락주세요.",
     "investment_scam", "base"),
    ("비트코인 상장 전 한정 사전 판매. 3일 안에 500% 수익 보장. 선착순 20명만 모집합니다.",
     "investment_scam", "base"),
    ("주식 리딩방 유료 가입 안내. 월 10% 수익률 실적. 지금 가입 시 첫 달 무료 체험.",
     "investment_scam", "base"),
    ("해외 부동산 선임대 프로젝트 한정 모집. 원금 보장 + 연 18% 배당. 관심 있으시면 상담 예약 주세요.",
     "investment_scam", "base"),
    ("신규 상장 알트코인 에어드랍 이벤트. 지금 지갑 주소 남기시면 500 토큰 무료 지급. 당첨 시 한화 80만원 상당.",
     "investment_scam", "base"),
    ("[공식] 삼성전자 임원 정보통. 내일 장 시작 전 반드시 매수. 목표가 100,000원. 전 재산 몰빵 추천.",
     "investment_scam", "base"),
    ("FX 마진 거래 AI 자동매매. 월 최소 30% 수익 보장. 손실 시 100% 환불. 데모계정 무료 지급.",
     "investment_scam", "base"),
    ("[Lg화학 한정] 내부자 추천 주식 내일상한가 90% 지금 입금 가능하신 분만",
     "investment_scam", "adversarial_char_substitute"),
    ("비 트 코 인 상 장 전 사 전 판 매 / 3일 / 500% 수 익 / 선 착 순",
     "investment_scam", "adversarial_spacing"),
    ("【LG𝐡𝐞𝐦𝐢𝐜𝐚𝐥 단톡】 내부정보 상한가90% 선입금500만 ₩즉시",
     "investment_scam", "adversarial_unicode_homoglyph"),
    # ========== loan_scam (5 base + 2 adversarial) ==========
    ("저금리 3.5% 특별 대출 상품 안내. 신용등급 무관 5천만원까지 당일 승인. 오늘 오후 4시까지만 모집: 010-XXXX-XXXX",
     "loan_scam", "base"),
    ("신용회복 전문 상담. 연체 기록 삭제 가능. 선수수료 30만원 입금 후 진행.",
     "loan_scam", "base"),
    ("금융위 인가 정책자금 대출. 신용등급 7등급 이하도 2천만원 가능. 조건 없이 즉시 승인.",
     "loan_scam", "base"),
    ("기존 대출 통합 대환 저금리 이벤트. 연 1.9% 특별 금리. 신청서만 보내주시면 10분 내 승인 안내드립니다.",
     "loan_scam", "base"),
    ("국책은행 특별대출 안내. 소득 증빙 불필요. 선입금 보증보험료 55만원만 있으면 3천만원 즉시 입금.",
     "loan_scam", "base"),
    ("저금리3.5%특별대출 신용무관 5천만 당일 010OOOOXXXX",
     "loan_scam", "adversarial_compressed"),
    ("정★책★자★금 대★출 인가 2천만 신용무관 즉시 → bit.ly/KOR-loan",
     "loan_scam", "adversarial_star_obfuscation"),
    # ========== subsidy_scam (5 base + 2 adversarial) ==========
    ("[정부24] 2026년 근로장려금 환급 대상자 최종 선정 안내. 아래 링크에서 본인인증 후 즉시 지급 가능: http://gov24-bonus.kr/refund",
     "subsidy_scam", "base"),
    ("건강보험공단입니다. 환급금 120만원이 발생했습니다. 본인인증 페이지에서 확인 바랍니다: http://hira-refund.com",
     "subsidy_scam", "base"),
    ("[국세청] 연말정산 추가 환급금 87만원 대기 중. 3일 이내 본인인증 진행: nts-korea.net",
     "subsidy_scam", "base"),
    ("[서울시청] 2026 긴급재난지원금 신청 대상자 확정. 아래 공식페이지에서 신청 바랍니다: seoul-covid-support.kr",
     "subsidy_scam", "base"),
    ("[고용노동부] 실업급여 미수령액 확인 바랍니다. 본인인증 후 자동 입금 처리됩니다: employment-refund.kr",
     "subsidy_scam", "base"),
    ("[정부 24] 근로 장려금 환급 대상. 링크 → gov24-bonus.kr/refund",
     "subsidy_scam", "adversarial_similar_domain"),
    ("[정부𝟤𝟦] 2026 근로장려금 120만원 환급. 아래 링크 본인인증: g﹒o﹒v﹒24-korea﹒net",
     "subsidy_scam", "adversarial_unicode_homoglyph"),
    # ========== family_impersonation (5 base + 3 adversarial) ==========
    ("엄마 나야. 폰이 고장나서 친구 폰으로 보내. 지금 급해서 그런데 100만원만 급하게 보내줄 수 있어?",
     "family_impersonation", "base"),
    ("아빠 나 민수야. 지금 친구랑 큰일이 생겼는데 급하게 50만원만 보내줘. 이따가 설명할게요.",
     "family_impersonation", "base"),
    ("할머니 저 손자예요. 폰 떨어뜨려서 액정 다 깨졌어요. 지금 수리비 30만원 입금해주시면 내일 바로 갚을게요.",
     "family_impersonation", "base"),
    ("엄마 이 계좌로 당장 200만원 부탁해. 카톡 답장 늦는 건 지금 병원이라 그래. 이따 설명할게.",
     "family_impersonation", "base"),
    ("누나 나야. 형한테 말하지 말고 나한테만 200만원 입금해줘. 진짜 부탁이야 다른 사람한테 얘기하지 말고.",
     "family_impersonation", "base"),
    ("엄마 나야 폰고장 친구폰 긴급 100만원 송금 부탁",
     "family_impersonation", "adversarial_compressed"),
    ("엄마ㅇㅣ야 폰고ㅈ ㅏㅇ 친구폰 긴급 100만원 ㅅ ㅗㅇㅁ ㅜㄴ 부탁",
     "family_impersonation", "adversarial_jamo_split"),
    ("𝗲𝗺𝗺𝗮 나야 폰 고장 100만원 ASAP 친구폰으로 보냄",
     "family_impersonation", "adversarial_unicode_code_mix"),
    # ========== benign (8) ==========
    ("내일 저녁 7시 강남역에서 만날까? 지난번에 얘기한 카페에서 보자.",
     "benign", "base"),
    ("[NH농협] 2026년 4월 5일 송금 50,000원 완료. 잔액 1,234,567원.",
     "benign", "base"),
    ("엄마 오늘 저녁에 뭐 먹고 싶어? 김치찌개 어때?",
     "benign", "base"),
    ("[택배] 고객님 주문하신 상품이 배송 완료되었습니다.",
     "benign", "base"),
    ("안녕 친구, 지난주에 빌린 책 다음주에 돌려줄게. 너무 재밌더라.",
     "benign", "base"),
    ("[Web발신] 신한카드 승인 13,500원 04/20 14:22 스타벅스 강남R점. 잔여한도 2,450,000원",
     "benign", "base"),
    ("안녕하세요. 저는 한국폴리텍대학 김교수입니다. 어제 세미나 질문 주신 내용 정리해서 이메일 드렸습니다.",
     "benign", "base"),
    ("안녕하세요 고객님, 주문하신 제품 색상이 일시품절되어 발송이 2일 지연될 수 있습니다. 양해 부탁드립니다.",
     "benign", "base"),
]


def run_demo(
    classifier: SolarClassifier | None = None,
    samples: list[tuple[str, ScamCategory, str]] | None = None,
    report_path: Path | None = None,
    json_path: Path | None = None,
) -> int:
    """Run the classifier on the sample battery and print a report table.

    Args:
        classifier: A SolarClassifier. Default creates from environment.
        samples: Optional custom samples override.
        report_path: Optional Markdown report output path.
        json_path: Optional JSON raw result output path.

    Returns:
        Exit code: 0 if primary-category F1 at or above threshold, 1 otherwise.
    """
    classifier = classifier or SolarClassifier()
    console = Console()
    samples = samples or SAMPLE_MESSAGES

    table = Table(
        title=f"HALO Layer 2 Demo — 6+1 Category Korean Scam Classifier (n={len(samples)})",
        show_lines=True,
    )
    table.add_column("#", width=3, style="dim")
    table.add_column("variant", style="blue")
    table.add_column("메시지 (앞 35자)", style="cyan", width=40)
    table.add_column("기대", style="yellow", width=22)
    table.add_column("예측", style="magenta", width=22)
    table.add_column("위험", justify="right", style="red", width=4)
    table.add_column("ms", justify="right", style="dim", width=5)

    results: list[dict[str, object]] = []
    per_category_correct: dict[str, int] = defaultdict(int)
    per_category_total: dict[str, int] = defaultdict(int)
    per_category_predicted: dict[str, int] = defaultdict(int)
    latencies: list[float] = []
    adversarial_correct = 0
    adversarial_total = 0

    for i, (message, expected, variant) in enumerate(samples, start=1):
        per_category_total[expected] += 1
        try:
            result = classifier.classify(message)
            is_correct = result.category == expected
            if is_correct:
                per_category_correct[expected] += 1
            per_category_predicted[result.category] += 1
            latencies.append(result.latency_ms)
            if variant != "base":
                adversarial_total += 1
                if is_correct:
                    adversarial_correct += 1

            mark = "✓" if is_correct else "✗"
            table.add_row(
                str(i),
                variant,
                message[:33] + ("..." if len(message) > 33 else ""),
                expected,
                f"{result.category} {mark}",
                str(result.risk_score),
                f"{result.latency_ms:.0f}",
            )
            results.append({
                "index": i,
                "variant": variant,
                "message": message,
                "expected": expected,
                "predicted": result.category,
                "correct": is_correct,
                "risk_score": result.risk_score,
                "rationale": result.rationale,
                "key_signals": result.key_signals,
                "latency_ms": result.latency_ms,
            })
        except (requests.RequestException, json.JSONDecodeError, KeyError) as exc:
            logger.error("classification failed for sample {}: {}", i, exc)
            table.add_row(
                str(i),
                variant,
                message[:33],
                expected,
                f"ERROR: {type(exc).__name__}",
                "-",
                "-",
            )
            results.append({
                "index": i,
                "variant": variant,
                "message": message,
                "expected": expected,
                "error": str(exc),
            })

    console.print()
    console.print(table)

    total = len(samples)
    n_correct = sum(per_category_correct.values())
    accuracy = n_correct / total if total else 0.0

    primary_f1s: list[float] = []
    for cat in PRIMARY_CATEGORIES:
        tp = per_category_correct[cat]
        fp = per_category_predicted[cat] - tp
        fn = per_category_total[cat] - tp
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        primary_f1s.append(f1)

    primary_f1_mean = sum(primary_f1s) / len(primary_f1s) if primary_f1s else 0.0
    latency_p50 = statistics.median(latencies) if latencies else 0.0
    adversarial_acc = (adversarial_correct / adversarial_total) if adversarial_total else 0.0

    console.print(
        f"\n[bold]전체 정확도: {n_correct}/{total} = {accuracy * 100:.1f}%[/bold]"
    )
    console.print(
        f"[bold]주요 3 카테고리 F1 평균: {primary_f1_mean:.3f}[/bold] "
        f"(대회 목표 ≥ 0.82)"
    )
    console.print(
        f"[bold]적대 변형 정확도: {adversarial_correct}/{adversarial_total} = "
        f"{adversarial_acc * 100:.1f}%[/bold]"
    )
    console.print(f"[dim]지연 p50: {latency_p50:.0f} ms (Solar-pro cloud API; "
                  "on-device 목표는 M2 측정)[/dim]")
    console.print(
        "\n[dim]이 데모는 Solar-pro API를 사용합니다. 최종 배포에서는 "
        "KT Mi:dm 2.0 Mini 2.3B + LoRA 어댑터를 기기 내에서 실행합니다.[/dim]"
    )

    if json_path:
        json_path.write_text(
            json.dumps(
                {
                    "samples": results,
                    "summary": {
                        "accuracy": accuracy,
                        "primary_f1_mean": primary_f1_mean,
                        "adversarial_accuracy": adversarial_acc,
                        "latency_p50_ms": latency_p50,
                        "total": total,
                        "correct": n_correct,
                    },
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        logger.info("JSON report written to {}", json_path)

    if report_path:
        report_path.write_text(_render_markdown_report(results, accuracy, primary_f1_mean,
                                                       adversarial_acc, latency_p50),
                               encoding="utf-8")
        logger.info("Markdown report written to {}", report_path)

    return 0 if primary_f1_mean >= 0.82 else 1


def _render_markdown_report(
    results: list[dict[str, object]],
    accuracy: float,
    primary_f1_mean: float,
    adversarial_acc: float,
    latency_p50: float,
) -> str:
    lines = [
        "# HALO Layer 2 Demo Report",
        "",
        "Cloud prototype against Upstage Solar-pro API. Production replaces",
        "this with on-device KT Mi:dm 2.0 Mini + LoRA adapter in M2.",
        "",
        "## Summary",
        "",
        f"- Samples: {len(results)}",
        f"- Accuracy: {accuracy * 100:.1f}%",
        f"- Primary 3 categories F1 mean: {primary_f1_mean:.3f}",
        f"- Adversarial accuracy: {adversarial_acc * 100:.1f}%",
        f"- Latency p50: {latency_p50:.0f} ms (cloud)",
        "",
        "## Per-sample",
        "",
        "| # | variant | expected | predicted | risk | rationale |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        rationale = str(r.get("rationale", ""))[:60].replace("|", "/")
        lines.append(
            f"| {r['index']} | {r.get('variant', '-')} | {r['expected']} | "
            f"{r.get('predicted', 'ERROR')} | {r.get('risk_score', '-')} | {rationale} |"
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--samples", type=Path, help="Optional JSON file of [text, category, variant] triples.")
    p.add_argument("--report", type=Path, help="Write Markdown report to this path.")
    p.add_argument("--json", type=Path, help="Write raw JSON results to this path.")
    p.add_argument("--model", default="solar-pro",
                   help="Upstage model name (solar-pro, solar-pro2, solar-pro3, solar-mini).")
    p.add_argument("--max-tokens", type=int, default=None,
                   help="Cap on generated tokens per response. Default is server-side.")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    samples = None
    if args.samples:
        data = json.loads(args.samples.read_text(encoding="utf-8"))
        samples = [(s["text"], s["category"], s.get("variant", "base")) for s in data]
    try:
        classifier = SolarClassifier(model=args.model, max_tokens=args.max_tokens)
        sys.exit(run_demo(classifier=classifier, samples=samples,
                          report_path=args.report, json_path=args.json))
    except ValueError as exc:
        logger.error(str(exc))
        sys.exit(2)


if __name__ == "__main__":
    main()
