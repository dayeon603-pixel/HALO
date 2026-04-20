# IRB Research Protocol Outline

_Target IRB: 국가생명윤리정책원 공용기관생명윤리위원회 (공용IRB)._
_Submission window: M1 of the HALO roadmap (2026-06)._
_Expected review duration: 2 to 4 months._
_Status: DRAFT outline. Sections marked TBD require Dayeon to fill_
_after consultation with 대한노인학회 advisor and law firm counsel._

---

## 1. Research title

HALO: On-device Korean sLLM Scam Defense Pilot with Elder Users at
성남시 어르신복지관.

## 2. Research team

| Role | Person | Affiliation |
|---|---|---|
| Principal Investigator | 강다연 (Dayeon Kang) | [ 소속 고등학교 ] + 성남시 청소년의회 의장 |
| Research Ethics Advisor | TBD | 대한노인학회 (자문 요청 예정) |
| Clinical Coordinator | TBD | 성남시 [ 복지관명 ] 담당자 |
| Legal Counsel | TBD | [ 법무법인명 ] |

Note: HALO is a solo-led research project with named external advisors.
PI is a high school student; 공용IRB review should apply standard
human-subjects protections with heightened protection for vulnerable
elderly participants.

## 3. Background and rationale

### 3.1 Public health and social impact

Korea's 2024 보이스피싱 피해액 reached 8,545억 원 (경찰청, historical
peak). Elderly populations (60+) account for approximately 25 percent
of victims and 35~40 percent of financial damage. Existing defense
systems (시티즌코난, T전화, AhnLab V3 Mobile) share three structural
limitations: blacklist lag, channel fragmentation, and absence of user
metacognition measurement.

### 3.2 Technology gap addressed

HALO provides a 4-layer on-device architecture combining KT Mi:dm 2.0
Mini for classification and a metacognition probe derived from the PI's
prior research (MetaMirage, Kaggle AGI Benchmark Challenge 2026,
submitted 2026-04-16).

### 3.3 Why pilot with elderly users

Elder populations experience higher per-incident financial loss and
limited prior exposure to evolving scam patterns. A pilot with this
population measures real-world efficacy in the group that most needs
protection.

## 4. Research hypotheses

### H1 (primary)

Soft intervention from HALO reduces the rate of positive user response
("계속 / 이체 진행") to confirmed scam patterns compared to no
intervention. Target: at least 30 percent reduction in a 3-month window.

### H2 (secondary)

User metacognitive calibration (Brier score) improves over the 3-month
pilot window with HALO feedback.

### H3 (exploratory)

Relationship-anomaly signals from Layer 3 detect long-term relational
scams (romance or investment) earlier than Layer 2 pattern alone.

## 5. Study design

### 5.1 Type

Prospective observational study with pre-post design. No randomization
in Y1 pilot (sample size 5~10 insufficient). Observational outcomes
only; no clinical intervention with medical consequences.

### 5.2 Sample size and justification

5 to 10 participants. Justification: exploratory pilot to measure feasibility
of HALO installation, UX, and preliminary effect sizes. Not powered for
hypothesis testing at statistical significance level. Full-scale efficacy
trial deferred to Phase 2.

### 5.3 Participant inclusion criteria

- Age 60 years or older.
- Owns and regularly uses an Android smartphone (minSDK 26, Android 8.0 or later).
- Receives Korean-language SMS messages at least weekly.
- Lives in 성남시 [ 복지관명 ] catchment area.
- Has at least one family member willing to assist with app setup.
- Capable of informed consent (or legal representative can consent).

### 5.4 Participant exclusion criteria

- Dementia or diagnosed cognitive impairment (per self-report or caregiver).
- Known severe vision impairment preventing use of smartphone UI.
- Active participation in another scam-prevention study.
- Unwilling or unable to participate in monthly in-person sessions.

### 5.5 Recruitment

- Through 성남시 어르신복지관 welcome desk and caregiver referral.
- Opt-in only; no compensation tied to data collection (nominal time
  compensation may be offered post-participation).
- Family member involvement encouraged for setup.

### 5.6 Study procedures

Week 0 (M4 start):
- In-person consent and enrollment session at 복지관.
- HALO Alpha app installation on participant's device with family help.
- Baseline survey (scam awareness, smartphone familiarity).

Weeks 1~12 (M4 through M6):
- Passive data collection via the HALO app (category, risk_score,
  rationale, user response). Raw message content remains device-local
  with 30-second ephemeral buffer.
- Weekly phone check-in (5 minutes) for UX feedback.
- Monthly in-person session at 복지관 (30 minutes) for Brier score
  review and UX iteration.

Week 13 (M6 end):
- Final in-person exit interview.
- Data export and device cleanup at participant request.
- Final survey.

### 5.7 Outcome measurements

Primary:
- Rate of positive user response to confirmed scam patterns
  (pre vs during pilot).

Secondary:
- Per-participant Brier score time series.
- Weekly retention (app-open events).
- Family notification reach rate (Phase 2 metric, partial in Y1).

Exploratory:
- Self-reported participant satisfaction.
- Qualitative UX observations.

## 6. Risk and benefit assessment

### 6.1 Risks

Category: Minimal risk. Approximate equivalent to using a standard
scam-prevention phone app.

Specific risks:
- Psychological: false-positive warnings may cause anxiety. Mitigation:
  clear warning language, counselor contact info, immediate family
  contact option.
- Privacy: sensitive message content processed on device. Mitigation:
  ephemeral buffer, no server transmission, opt-in metadata only.
- Dependency: user may over-rely on HALO. Mitigation: warnings include
  guidance to also consult family; pilot length limited to 3 months.
- Data breach: device loss or theft. Mitigation: encrypted SQLite
  storage, 90-day automatic data expiration.

### 6.2 Benefits

Direct to participants:
- Real-time scam warning on personal device.
- Digital safety literacy improvement via interaction.
- Immediate family contact pathway in Phase 2 rollout.

Indirect (societal):
- Contribution to open-source Korean scam defense research.
- Evidence base for 복지관 digital safety programs.
- Model for 전국 확산 in 2027 plus.

### 6.3 Risk-benefit balance

Minimal risks are outweighed by direct protective benefit and indirect
research value. Participants can withdraw at any time.

## 7. Data management plan

### 7.1 What data is collected

On device (encrypted SQLite, 90-day retention):
- event_id (UUID)
- timestamp
- channel (SMS or URL in Y1)
- salted_sender_hash (no raw phone number)
- classifier category
- risk_score
- user response (continue / stop / family_notified)
- user_confidence_1_to_10 (Layer 3 probe response)
- response_time_ms

On server (opt-in aggregated telemetry):
- daily counts per category
- aggregate risk distributions
- no PII, no raw content

Survey responses (paper or electronic, PI-managed):
- demographics (age range, sex, approximate education level)
- scam awareness pre and post
- satisfaction and UX qualitative

### 7.2 Storage and access

- Device data: encrypted at rest on participant device only.
- Exit export: participant's choice of format (JSON, CSV, or opt out).
- Research data in PI's management: encrypted hard drive, access
  limited to PI and named IRB-listed advisors.
- No cloud storage of device data.

### 7.3 Retention and destruction

- Device data: 90 days rolling retention, automatic purge.
- Research data: retained for 5 years per research-records norm, then
  securely destroyed.
- Participant can request earlier destruction at any time.

## 8. Informed consent

### 8.1 Consent process

Three-step consent:
1. Information session at 복지관 with opportunity for questions.
2. Written consent form signed by participant (or legal representative).
3. Family assent form signed by at least one family member who will
   assist with app setup.

Consent language:
- Plain Korean, 14pt font minimum, large print available.
- Accessible reading level (no jargon).
- Emphasizes voluntary nature and withdrawal right.

### 8.2 Consent form sections

- Study purpose
- Procedures
- Risks and discomforts
- Benefits
- Alternatives to participation (declining)
- Confidentiality
- Voluntary participation and withdrawal
- Compensation (if any)
- Contact for questions
- Signature and date

### 8.3 Language and literacy accommodations

Simplified language version for participants with lower literacy.
Verbal explanation by coordinator as needed.

## 9. Monitoring and adverse event reporting

### 9.1 Monitoring

- Weekly participant check-ins (phone).
- Monthly in-person sessions.
- PI reviews event logs weekly.

### 9.2 Adverse event definition

- Any false-positive HALO warning that caused the participant to
  decline a legitimate communication with negative consequences.
- Any privacy incident.
- Any psychological distress reported by participant or family.

### 9.3 Reporting timeline

- Serious adverse event: reported to IRB within 24 hours.
- Minor adverse event: reported in monthly summary.
- Protocol deviation: reported in monthly summary.

### 9.4 Stopping rules

Study pauses if:
- More than 2 participants withdraw due to app issues within first month.
- Any serious adverse event occurs.
- Privacy incident of any kind.

## 10. Funding and resources

Research is self-funded by the PI for Y1. No external grant dependency.
Possible in-kind support:
- NIPA (National IT Industry Promotion Agency) GPU resources for model
  training through 2026 AI Champion 대회 제14조 ③ support.
- 성남시 복지관 space and coordination assistance.

No financial relationships between PI and any commercial scam-prevention
vendor.

## 11. Conflicts of interest

PI reports:
- No employment relationship with KT, Upstage, or any 연계 기업.
- No financial compensation from any data source or advisory party.
- Research is conducted independently for academic and civic value.

## 12. Dissemination plan

Intended outputs:
- ACL 2027 or EMNLP 2027 methodology paper on LLM metacognition
  transfer to human users.
- NeurIPS 2027 Datasets and Benchmarks paper on Korean Multi-channel
  Scam Probe Suite.
- CHI 2027 HCI paper on intergenerational intervention protocols.
- Open-source release of halo-probe-suite under Apache 2.0.
- Policy brief for 과학기술정보통신부 on high-risk AI evaluation.
- Public report to 성남시 on pilot outcomes (with complex consent).

Privacy in publications:
- No identifying information.
- Quotations anonymized.
- Aggregate statistics only unless separate explicit consent.

## 13. References

Key supporting documents:
- `docs/whitepaper.md`: full technical design.
- `docs/privacy.md`: legal and privacy architecture.
- `docs/metacognition.md`: MetaMirage transfer methodology.
- 경찰청 공공데이터포털: boivoice phishing statistics.
- APWG 2024, GASA 2023: international context.

---

## Checklist for submission

- [ ] Complete Section 2 (research team advisor names).
- [ ] Complete Section 3.3 (legal counsel name and law firm).
- [ ] Prepare informed consent form in final language.
- [ ] Prepare family assent form.
- [ ] Prepare baseline and exit survey instruments.
- [ ] Obtain letter of cooperation from 성남시 복지관.
- [ ] Verify encrypted storage system on PI laptop.
- [ ] Complete CITI Program or equivalent human-subjects training and
      attach certificate.
- [ ] Submit complete package to 공용IRB via online portal.

## Timeline

- 2026-06-01: submission package draft complete.
- 2026-06-15: submission to 공용IRB.
- 2026-08 to 2026-09: IRB review, respond to reviewer comments.
- 2026-09-01 target: IRB approval.
- 2026-09-15 target: pilot enrollment begins.
- 2026-11-30: pilot concludes.
