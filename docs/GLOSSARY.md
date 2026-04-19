# HALO Glossary

Terminology used across HALO documentation.

## A

**Abstention**: The system choice to not answer or not act because confidence is below a safety threshold. In HALO Layer 4, abstention manifests as Soft or higher intervention.

**AI 기본법**: The Korean Framework Act on AI, enacted 2025-01-21, enforced 2026-01-22. Mandates safety assessments for high-risk AI.

## B

**Brier Score**: Mean squared error between predicted probability and actual outcome. Used in Layer 3 to measure user metacognitive calibration.

## E

**ECE**: Expected Calibration Error. Measures how well a model's confidence scores match its actual accuracy.

**Ephemeral buffer**: Memory region holding raw input for at most 30 seconds before automatic clearing. Protects user privacy.

## G

**GPTQ**: Gradient-based Post-Training Quantization. HALO uses GPTQ INT4 to compress Mi:dm 2.0 Mini for mobile deployment.

## I

**IRB**: Institutional Review Board. HALO pilot uses 공용IRB (Public IRB at 국가생명윤리정책원).

## L

**LoRA**: Low-Rank Adaptation. Parameter-efficient fine-tuning technique used in HALO for scam classification.

## M

**Mi:dm 2.0 Mini**: KT's 2.3B parameter Korean LLM (HuggingFace: K-intelligence/Midm-2.0-Base-Instruct). HALO's primary on-device classifier.

**MetaMirage**: HALO team lead's 2026 Kaggle AGI Benchmark Challenge submission. Found r = −0.84 sign-flip correlation between LLM capability and metacognitive accuracy on engineered task families.

## O

**ONNX**: Open Neural Network Exchange. Interoperable model format used for mobile deployment.

## Q

**QNN**: Qualcomm Neural Network SDK. Accelerates on-device inference on Snapdragon NPU.

## R

**Risk Engine**: Layer 3 component that combines pattern classification score, user confidence deviation, and relationship anomaly into a single 0~100 risk value.

## S

**Solar-pro**: Upstage's large Korean LLM accessed via API. HALO cloud helper for long-form analysis and auto report generation.

**SPS Framework**: Structured Perturbation Stability Framework. Team IP used to generate adversarial corpus variants for scam detection robustness.

## T

**TRL**: Technology Readiness Level. HALO is at TRL 3 to 4 at proposal time, targeting TRL 5 after M6 pilot.

**통비법**: 통신비밀보호법. Korean Protection of Communications Secrets Act. Article 3 restricts voice interception.

## V

**Verbalized Confidence**: User self-reported confidence on a 1 to 10 scale. Core Layer 3 signal.
