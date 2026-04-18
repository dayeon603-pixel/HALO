# HALO Roadmap

Y1 phase (the competition window, 2026-06 to 2026-11) is scoped for solo
execution at roughly 30 hours per week, totaling 780 engineering hours.
Phase 2 captures deferred work that extends the prototype into a full
product.

## Y1 Phase 1 monthly plan

### M1 — 2026-06 (130 hr budget)

Primary outcomes:
- Korean scam corpus v0 with 300+ labeled examples across 6+1 categories.
- Mi:dm 2.0 Mini local environment set up for fine-tuning.
- 공용IRB submission prepared and filed.
- 성남시 어르신복지관 formal cooperation inquiry sent through 청소년의회 channel.

Activities:
- Collect data from 경찰청 press releases, KISA advisories, 금감원 reports, community posts.
- Annotate 300+ examples with category plus 3 key signals each.
- Generate SPS adversarial perturbations for 20% of corpus.
- Draft IRB research plan, informed consent, privacy policy, risk assessment.
- Set up PyTorch, Transformers, PEFT, Datasets on local MacBook Pro and NIPA GPU.

Phase gate criteria:
- Corpus is labeled with documented protocol.
- IRB submission is confirmed received.

### M2 — 2026-07 (130 hr budget)

Primary outcomes:
- Mi:dm 2.0 Mini LoRA model v0 with measured F1 per category.
- Galaxy S24 on-device latency benchmark for INT4 quantized model.
- Legal counsel engagement initiated for 통신비밀보호법 analysis.

Activities:
- LoRA fine-tune Mi:dm 2.0 Mini on 300-sample corpus using NIPA A100.
- Evaluate on held-out test set. Report F1, precision, recall, ECE per category.
- ONNX export with Optimum. Apply GPTQ 4-bit quantization.
- Deploy to Galaxy S24 via ONNX Runtime Mobile 1.24. Measure p50 latency on SMS-length inputs.
- Engage a law firm for written opinion on voice channel legality.

Phase gate criteria:
- F1 ≥ 0.82 on primary 3 categories, or documented shortfall and corpus expansion plan.
- Measured on-device p50 latency reported.

### M3 — 2026-08 (150 hr budget)

Primary outcomes:
- Android MVP Alpha with SMS channel and Soft intervention.
- Risk Engine v0 integrating Layer 2 classification and Layer 3 placeholder.
- Corpus v1 expanded to 500+ samples.

Activities:
- Kotlin application scaffold with Jetpack Compose UI.
- BroadcastReceiver for SMS intake.
- ONNX Runtime Mobile integration with the Mi:dm INT4 checkpoint.
- Foreground Service orchestrating Layer 1 to Layer 4 pipeline.
- Full-screen Soft intervention overlay with rationale display.
- Corpus expansion by 200 examples with quality review.

Phase gate criteria:
- APK installable on Galaxy S24 and runs end-to-end on a received SMS.

### M4 — 2026-09 (130 hr budget)

Primary outcomes:
- 공용IRB approval received.
- 성남시 복지관 cooperation letter received.
- Pilot recruitment and onboarding complete with 5~10 elder users.

Activities:
- Follow up on IRB. Respond to reviewer comments.
- In-person meeting with 성남시 복지관 담당과 for operational details.
- Recruit participants. Obtain informed consent from participants and, where appropriate, caregivers.
- Install HALO Alpha on participant devices, with family-assisted setup.
- Begin 3-month observation window.

Phase gate criteria:
- IRB approval documented.
- At least 5 participants recruited, consented, and onboarded.

### M5 — 2026-10 (130 hr budget)

Primary outcomes:
- Mid-pilot data collection and analysis.
- Layer 3 metacognition probe fully integrated.
- Weekly retention and Soft intervention acceptance logged.

Activities:
- Daily automated check of classification events.
- Weekly phone or in-person check-in with participants.
- UX iteration based on observed friction.
- Interim analysis of Brier scores and relationship-anomaly signals.

Phase gate criteria:
- Pilot data collection is proceeding without attrition beyond expectation.
- Interim Brier scores available for assessment.

### M6 — 2026-11 (110 hr budget)

Primary outcomes:
- Final pilot analysis with F1, Brier, and incident outcomes.
- Halo-probe-suite public release (license TBD pending competition conclusion).
- Written whitepaper update and policy brief.
- Competition finals presentation materials ready.

Activities:
- Lock pilot data. Run final analysis.
- Write pilot report with findings, limitations, next steps.
- Prepare final submission video and presentation.
- Package halo-probe-suite.
- Finalize Phase 2 plan.

Phase gate criteria:
- Final pilot data reported.
- Submission-ready presentation.

## Phase 2 (post-competition or parallel)

Deferred from Y1:

- Voice call channel with legal counsel sign-off.
- Messenger (KakaoTalk) channel after Play Store policy review.
- Bank app screen channel.
- Medium and Hard intervention levels.
- Family Companion Web application.
- iOS port.
- Japanese LoRA adapter with NTT Tsuzumi 2 base.
- English LoRA adapter with Llama 3.2 1B base.
- 나라장터 공공조달 certification and 보안성 검토.
- Series A funding round preparation.

## Long-term milestones

- 2027 Q1: Japan pilot if partnership secured.
- 2027 Q2~Q3: Methodology paper submission to ACL or EMNLP.
- 2027 Q4: Open beta on Play Store.
- 2028 Q1: 공공조달 registration attempt.
- 2028 Q2: 1st B2G contract target.
- 2029 onward: global market entry scaled with local partnerships.

## Success metrics at Y1 end

- Pilot zero-incident outcome.
- F1 primary 3 ≥ 0.82.
- Brier score decreasing across pilot window.
- Complete IRB, legal, and privacy paper trail.
- Open benchmark released.
- Finals presentation delivered.
