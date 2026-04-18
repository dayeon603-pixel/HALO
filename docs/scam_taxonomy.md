# Korean Scam Taxonomy (6+1 Categories)

HALO classifies incoming Korean text into one of six scam categories or a
benign class. This document defines each category with operational criteria
and representative examples. The taxonomy informs corpus collection, LoRA
fine-tuning labels, and Layer 4 intervention messages.

All examples are synthetic, based on publicly reported cases from 경찰청
press releases and KISA 인터넷침해대응센터 advisories. Personal identifiers
have been removed or replaced with placeholders.

## 1. voice_phishing (보이스피싱)

Definition: impersonation of a public institution or financial institution
to coerce the recipient into financial transfers or account access.

Common scripts:
- 검찰 수사관·검사 사칭 ("귀하의 계좌가 금융사기에 연루되어...")
- 금감원·금융기관 사칭 ("대환 대출 신청이 접수되었습니다...")
- 건강보험공단·국세청 사칭 ("환급금이 발생하여 안내드립니다...")

Key signals:
- Urgency imposed by an institutional authority.
- Request to install an app, visit a URL, or transfer funds to verify.
- Threat of legal consequence if the recipient does not comply.

Example:
> 서울중앙지방검찰청 김철수 검사입니다. 귀하의 계좌가 금융사기 사건에
> 연루되어 즉시 확인이 필요합니다. 아래 번호로 지금 바로 연락 부탁드립니다.

## 2. romance_scam (로맨스 스캠)

Definition: relationship building over days to months followed by financial
requests under pretexts such as travel emergencies, investment partnerships,
or medical costs.

Common scripts:
- 해외 파견 근무자 위장 (군인, 의사, 엔지니어)
- 결혼 이야기로 진행하다 갑작스런 사고나 비용 문제

Key signals:
- Initial contact from a plausible but unverifiable identity.
- Rapid intimacy escalation.
- Funds request under emotional stress.

Example:
> 해외 파견 근무 중인 미군 의사입니다. 시리아 임무 중 귀하의 따뜻한
> 메시지에 위로를 받고 있습니다. 친구가 되어주실래요?

## 3. investment_scam (투자·코인 사기)

Definition: promise of extraordinary returns from undisclosed private
information, exclusive investment groups, or crypto projects.

Common scripts:
- 내부자 정보 단체 카톡방 초대
- 신규 코인 상장 전 한정 투자 기회
- 리딩방 (유료 투자 조언방)

Key signals:
- Guaranteed high returns.
- Exclusivity framing (limited seats, insider access).
- Pressure to transfer funds to an external wallet.

Example:
> 【LG화학 단체카톡】 내부자 추천 특급 정보.
> 내일 상한가 90% 확실. 선입금 500만원 가능하신 분만 연락주세요.

## 4. loan_scam (대출 사기)

Definition: offers of low-interest loans that require upfront fees or lead
to identity theft.

Common scripts:
- 저금리 특별 대출 상품 안내
- 신용등급 회복 서비스
- 대환 대출로 부채 통합

Key signals:
- Interest rates far below market.
- "Credit rating recovery" services for upfront fees.
- Collection of personal financial information.

Example:
> 저금리 3.5% 특별 대출 상품 안내. 신용등급 무관 5천만원까지 당일 승인.
> 오늘 오후 4시까지만 모집: 010-XXXX-XXXX

## 5. subsidy_scam (지원금·환급 사칭)

Definition: impersonation of government programs to steal identity
information or redirect funds through fake portals.

Common scripts:
- 근로장려금 환급 안내
- 코로나 지원금 신청 연장
- 건강보험 환급금 수령 안내

Key signals:
- Links to domains that mimic gov.kr or 정부24.
- Requests for identity verification on untrusted pages.
- Tight deadline pressure.

Example:
> [정부24] 2026년 근로장려금 환급 대상자 최종 선정 안내.
> 아래 링크에서 본인인증 후 즉시 지급 가능: http://gov24-bonus.kr/refund

## 6. family_impersonation (가족 사칭)

Definition: attacker claims to be a family member in distress and requests
immediate financial assistance.

Common scripts:
- "엄마 나야, 폰이 고장나서..."
- "아빠, 친구랑 문제 생겼어..."
- 교통사고·수술비 긴급 송금 요청

Key signals:
- New or unrecognized number.
- Broken phone excuse.
- Request to transfer funds to a third-party account.

Example:
> 엄마 나야. 폰이 고장나서 친구 폰으로 보내. 지금 급해서 그런데
> 100만원만 급하게 보내줄 수 있어? 내 계좌로 바로 돌려드릴게.

## 7. benign (정상 메시지)

Definition: all other legitimate communications. Approximately 50% of the
training corpus to balance the classifier and minimize false positives.

Examples:
> 내일 저녁 7시 강남역에서 만날까?
> [NH농협] 2026년 4월 5일 송금 50,000원 완료.
> 엄마 오늘 저녁 반찬 뭐 먹지

## Adversarial variations (SPS-style)

For every base sample, up to 20% of the corpus is expanded with adversarial
perturbations to train robust recognition.

Perturbation types:
- Emoji or whitespace insertion: `서울중앙지✨검✨` vs `서울중앙지검`
- Character substitution: `Lg화학` vs `LG화학`
- Similar domain: `gov24-bonus.kr` vs `gov.kr`
- Context reordering while preserving meaning.

See `docs/evaluation.md` for ablation of adversarial augmentation impact on F1.

## Labeling protocol

1. Primary labeling by the team lead.
2. Secondary review of 10% sample by KISA or 대한노인학회 advisory.
3. Label consistency target Cohen's κ ≥ 0.75.
4. Ambiguous samples flagged and excluded or separately stored.

## References

- 경찰청 사이버수사국 보도자료 아카이브.
- KISA 인터넷침해대응센터 공개 경보.
- 금감원 보이스피싱 실태조사 보고서.
