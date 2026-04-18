"""HALO — Holistic Agent for Local-inference Observation.

Real-time, on-device Korean sLLM scam-defense agent with metacognitive calibration.

Architecture (4-Layer):
    1. SENSING — 5-channel ingestion (SMS, voice, messenger, screen, URL)
    2. CLASSIFICATION — On-device Korean sLLM (Solar-mini + LoRA)
    3. METACOGNITION PROBE — MetaMirage-based user confidence calibration
    4. INTERVENTION — 3-stage escalation (Soft / Medium / Hard) + family connect

Research foundation:
    - MetaMirage (Kaggle AGI Benchmark Challenge 2026, submitted 2026-04-16)
    - Structured Perturbation Stability Framework
"""

__version__ = "0.1.0"
__author__ = "Dayeon Kang"
__all__ = ["__version__"]
