# HALO Layer 2 Demo Report

Cloud prototype against Upstage Solar-pro API. Production replaces
this with on-device KT Mi:dm 2.0 Mini + LoRA adapter in M2.

## Summary

- Samples: 25
- Accuracy: 88.0%
- Primary 3 categories F1 mean: 0.869
- Adversarial accuracy: 100.0%
- Latency p50: 899 ms (cloud)

## Per-sample

| # | variant | expected | predicted | risk | rationale |
|---|---|---|---|---|---|
| 1 | base | voice_phishing | voice_phishing | 95 | 검찰청 소속 검사 사칭과 계좌 연루 확인을 요구하는 전형적인 보이스피싱 패턴 |
| 2 | base | voice_phishing | family_impersonation | 95 | 가족 구성원을 사칭하며 긴급한 금전적 요구를 하는 전형적인 사기 패턴입니다. 실제 사고 상황을 확인할 수 없 |
| 3 | base | voice_phishing | voice_phishing | 95 | 금융감독원 및 수사관 사칭, 불법 대출 명목의 긴급성 강조로 보이스피싱의 전형적 패턴 |
| 4 | base | voice_phishing | subsidy_scam | 85 | 국세청 체납 담당을 사칭하며 체납 세금 미납 시 자산 동결을 경고하는 내용으로, 정부 기관을 사칭한 지원금/ |
| 5 | adversarial_emoji_spacing | voice_phishing | voice_phishing | 95 | 기관명(검찰청)과 직책(검사)을 사칭하며 계좌 확인을 요구하는 전형적인 보이스피싱 패턴입니다. 특수문자(✨) |
| 6 | base | romance_scam | romance_scam | 65 | 과거 만남을 언급하며 친밀감을 조성하고, 해외 상황을 이용해 접근하며 향후 금전 요구로 이어질 가능성이 있는 |
| 7 | base | romance_scam | romance_scam | 85 | 고독한 상황을 이용해 친밀감을 형성하고 특별한 관계를 요구하는 전형적인 로맨스 스캠 패턴 |
| 8 | base | romance_scam | investment_scam | 75 | 고수익 투자 유도와 해외 전문가 사칭 등 투자 사기 전형적 패턴 확인됨. 구체적 사업 내용 없이 신뢰만 강조 |
| 9 | base | investment_scam | investment_scam | 95 | 고수익 보장(90% 상한가)과 선입금을 요구하는 점이 투자 사기의 전형적 특징입니다. 내부자 정보를 강조하며 |
| 10 | base | investment_scam | investment_scam | 95 | 고수익 보장(500%)과 한정된 기회(선착순 20명)를 강조하는 투자 권유는 전형적인 투자 사기 수법입니다. |
| 11 | base | investment_scam | investment_scam | 85 | 고수익(10%)을 보장하며 유료 가입을 유도하는 투자 사기 전형적 패턴. '실적' 강조와 무료 체험은 신뢰성 |
| 12 | adversarial_char_substitute | investment_scam | investment_scam | 95 | 고수익 보장(90% 상한가)과 내부자 정보를 강조하며, 특정 기업(LG화학)을 언급한 투자 유도 메시지로 전 |
| 13 | base | loan_scam | loan_scam | 85 | 저금리 특별 대출, 신용등급 무관, 당일 승인, 시간 제한 등 대출 사기의 전형적 키워드를 포함하고 있으며, |
| 14 | base | loan_scam | loan_scam | 95 | 신용회복 및 연체 기록 삭제를 명목으로 선수수료를 요구하는 것은 대출 사기의 전형적인 수법입니다. 실제 신용 |
| 15 | base | subsidy_scam | subsidy_scam | 95 | 정부기관 사칭과 가짜 링크를 통해 지원금 환급을 유도하는 전형적인 사기 수법이며, 공식 도메인과 일치하지 않 |
| 16 | base | subsidy_scam | subsidy_scam | 95 | 정부기관(건강보험공단)을 사칭하며 환급금을 미끼로 한 URL 유도, 공식 도메인과 다른 의심스러운 링크 포함 |
| 17 | adversarial_similar_domain | subsidy_scam | subsidy_scam | 85 | 정부 기관을 사칭한 지원금 환급 메시지로, 공식 도메인과 다른 의심스러운 링크가 포함되어 있습니다. |
| 18 | base | family_impersonation | family_impersonation | 85 | 가족을 사칭하며 긴급한 송금을 요구하는 전형적인 패턴이며, 개인 기기 문제(폰 고장)를 이유로 제시하고 있습 |
| 19 | base | family_impersonation | family_impersonation | 85 | 자녀를 사칭하며 긴급한 송금을 요구하는 전형적인 가족 사칭 사기 패턴입니다. 실제 자녀라면 구체적인 상황 설 |
| 20 | adversarial_compressed | family_impersonation | family_impersonation | 95 | 가족을 사칭하며 긴급한 송금을 요청하는 전형적인 사기 패턴입니다. '폰고장', '친구폰', '긴급 송금' 등 |
| 21 | base | benign | benign | 10 | 일상적인 만남 제안으로 사기 관련 키워드나 위험 신호가 전혀 없습니다. |
| 22 | base | benign | benign | 10 | 농협 계좌의 정상적인 거래 내역 알림으로, 사기 관련 키워드나 유도 행위가 없음 |
| 23 | base | benign | benign | 0 | 일상적인 가족 간 대화 내용으로, 금전 요구나 사기 관련 키워드가 전혀 없습니다. |
| 24 | base | benign | benign | 10 | 택배 배송 완료 알림은 일상적인 상거래 메시지로, 사기 관련 키워드나 위험 신호가 없습니다. |
| 25 | base | benign | benign | 0 | 책을 빌려주고 돌려준다는 일상적인 대화로 사기 관련 키워드나 위험 신호가 전혀 없습니다. |
