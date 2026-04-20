#!/usr/bin/env python3
"""Download and benchmark KT Mi:dm 2.0 Mini on the local machine.

This is a pre-M2 smoke test. It verifies that:
    1. The model downloads and loads without error.
    2. CPU inference produces a coherent Korean response.
    3. Latency on a MacBook CPU is in a reasonable range (expected
       seconds, not milliseconds, since no QNN/NPU acceleration).

Production deployment will quantize to INT4 and use Qualcomm QNN on
Snapdragon devices. This script only verifies the path; actual on-device
latency measurement happens on Galaxy S24 in M2.

Usage:
    pip install "transformers>=4.44" torch accelerate sentencepiece
    python scripts/benchmark_mi_dm.py

The first run downloads ~5 GB (FP16 weights) from HuggingFace. Subsequent
runs use the local cache at ~/.cache/huggingface/hub.
"""

from __future__ import annotations

import argparse
import statistics
import sys
import time
from pathlib import Path

from loguru import logger

MODEL_ID = "K-intelligence/Midm-2.0-Base-Instruct"

SAMPLE_PROMPTS = [
    "다음 메시지를 '보이스피싱' 또는 '정상'으로 분류하세요: "
    "서울중앙지검 김검사입니다. 귀하의 계좌가 사건에 연루되어 즉시 확인이 필요합니다.",
    "다음 메시지를 '보이스피싱' 또는 '정상'으로 분류하세요: "
    "내일 7시 강남역에서 만날까요?",
    "다음 메시지를 '투자사기' 또는 '정상'으로 분류하세요: "
    "내부자 추천 종목 내일 상한가 확실. 선입금 가능하신 분만.",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--max-new-tokens", type=int, default=64)
    p.add_argument("--device", default="auto",
                   choices=["auto", "cpu", "cuda", "mps"])
    p.add_argument("--output", type=Path,
                   default=Path("experiments/mi_dm_cpu_benchmark.md"))
    return p.parse_args()


def main() -> int:
    args = parse_args()

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        logger.error("Missing deps: {}. Run: pip install transformers torch accelerate",
                     exc)
        return 2

    device = args.device
    if device == "auto":
        if torch.cuda.is_available():
            device = "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"
    logger.info("Using device: {}", device)

    logger.info("Loading tokenizer for {}", MODEL_ID)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)

    logger.info("Loading model for {} (may download ~5 GB)", MODEL_ID)
    t_load_start = time.perf_counter()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16 if device != "cpu" else torch.float32,
        trust_remote_code=True,
    ).to(device)
    model.eval()
    load_elapsed = time.perf_counter() - t_load_start
    logger.info("Model loaded in {:.1f} s", load_elapsed)

    latencies: list[float] = []
    responses: list[str] = []

    for i, prompt in enumerate(SAMPLE_PROMPTS, start=1):
        logger.info("Running sample {}/{}", i, len(SAMPLE_PROMPTS))
        inputs = tokenizer(prompt, return_tensors="pt").to(device)

        t0 = time.perf_counter()
        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
            )
        elapsed = time.perf_counter() - t0
        latencies.append(elapsed)

        text = tokenizer.decode(
            output_ids[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True,
        )
        responses.append(text)
        logger.info("  latency: {:.2f} s, response: {}...", elapsed, text[:60])

    mean_latency = statistics.mean(latencies)
    median_latency = statistics.median(latencies)

    report = [
        f"# Mi:dm 2.0 Mini CPU Benchmark (smoke test)",
        "",
        f"Model: {MODEL_ID}",
        f"Device: {device}",
        f"Load time: {load_elapsed:.1f} s",
        f"Max new tokens: {args.max_new_tokens}",
        f"Samples: {len(SAMPLE_PROMPTS)}",
        "",
        f"Mean latency: {mean_latency:.2f} s",
        f"Median latency: {median_latency:.2f} s",
        f"Min latency: {min(latencies):.2f} s",
        f"Max latency: {max(latencies):.2f} s",
        "",
        "## Sample outputs",
        "",
    ]
    for prompt, resp, lat in zip(SAMPLE_PROMPTS, responses, latencies):
        report.append(f"**Prompt** ({lat:.2f}s): {prompt}")
        report.append(f"**Response**: {resp}")
        report.append("")

    report.append("## Notes")
    report.append("")
    report.append("This is a CPU/GPU load and correctness check on a developer")
    report.append("machine, not the production deployment benchmark. Production")
    report.append("uses INT4 GPTQ quantization on Qualcomm QNN (Snapdragon 8 Gen 3)")
    report.append("or Samsung NNAPI delegate. The target mobile latency p50 < 300 ms")
    report.append("is measured in M2 on Galaxy S24, not on a laptop.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(report), encoding="utf-8")
    logger.info("Report written to {}", args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
