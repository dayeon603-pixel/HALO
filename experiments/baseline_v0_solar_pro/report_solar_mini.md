# HALO Layer 2 Demo Report

Cloud prototype against Upstage Solar-pro API. Production replaces
this with on-device KT Mi:dm 2.0 Mini + LoRA adapter in M2.

## Summary

- Samples: 25
- Accuracy: 88.0%
- Primary 3 categories F1 mean: 0.869
- Adversarial accuracy: 100.0%
- Latency p50: 1392 ms (cloud)

## Per-sample

| # | variant | expected | predicted | risk | rationale |
|---|---|---|---|---|---|
| 1 | base | voice_phishing | voice_phishing | 95 | 검찰청 사칭 및 계좌 확인 요청은 전형적인 보이스피싱 수법입니다. |
| 2 | base | voice_phishing | family_impersonation | 85 | 가족 사칭 사기의 전형적인 수법으로, 긴급한 상황을 언급하며 금전을 요구합니다. |
| 3 | base | voice_phishing | voice_phishing | 90 | 금융감독원 사칭 및 긴급 조치 요구는 전형적인 보이스피싱 수법입니다. |
| 4 | base | voice_phishing | subsidy_scam | 85 | 국세청 사칭 및 자산 동결 위협으로 지원금 사칭 가능성이 높음 |
| 5 | adversarial_emoji_spacing | voice_phishing | voice_phishing | 90 | 메시지가 서울중앙지검 검사를 사칭하고 계좌 확인을 부탁하는 내용이므로 보이스피싱 가능성이 높습니다. |
| 6 | base | romance_scam | romance_scam | 50 | 해외 파견 중이라는 상황과 한국 분이라는 점을 강조하며 친밀감을 형성하려는 시도가 로맨스 스캠의 전형적인 수 |
| 7 | base | romance_scam | romance_scam | 75 | 시리아 임무 중인 미군 대위를 사칭하며 고독함을 강조하고 특별한 관계를 제안하는 것은 로맨스 스캠의 전형적인 |
| 8 | base | romance_scam | investment_scam | 70 | 해외 유전 투자 제안은 고수익을 미끼로 한 사기일 가능성이 높습니다. |
| 9 | base | investment_scam | investment_scam | 85 | 내부자 정보를 이용한 주식 투자를 제안하며 선입금을 요구하는 것은 전형적인 투자 사기 수법입니다. |
| 10 | base | investment_scam | investment_scam | 85 | 비트코인 상장 전 한정 사전 판매와 3일 안에 500% 수익 보장은 전형적인 투자 사기 패턴입니다. |
| 11 | base | investment_scam | investment_scam | 70 | 고수익을 보장하는 주식 리딩방 유료 가입 권유로 투자 사기 가능성이 있음. |
| 12 | adversarial_char_substitute | investment_scam | investment_scam | 85 | 내부자 추천, 상한가 보장 등 비현실적인 투자 정보를 제공하며 입금을 유도하는 전형적인 투자 사기 패턴입니다 |
| 13 | base | loan_scam | loan_scam | 85 | 저금리 특별 대출 상품 안내와 신용등급 무관, 당일 승인 등의 표현은 대출 사기의 전형적인 신호입니다. |
| 14 | base | loan_scam | loan_scam | 85 | 신용 회복을 위한 선수수료 요구는 전형적인 대출 사기의 수법입니다. |
| 15 | base | subsidy_scam | subsidy_scam | 85 | 정부 기관을 사칭하여 환급을 미끼로 한 사기 가능성이 높습니다. |
| 16 | base | subsidy_scam | subsidy_scam | 85 | 정부기관 사칭 및 환급금 발생을 이유로 링크 접속을 유도하는 것으로 보아 지원금 사칭의 가능성이 높습니다. |
| 17 | adversarial_similar_domain | subsidy_scam | subsidy_scam | 85 | 정부 기관을 사칭하여 환급을 언급하고 있으며, 제공된 URL이 공식적인 정부 도메인이 아닙니다. |
| 18 | base | family_impersonation | family_impersonation | 70 | 자녀를 사칭하며 긴급한 금전 지원을 요청하는 메시지로, 가족 사칭형 사기 가능성이 높습니다. |
| 19 | base | family_impersonation | family_impersonation | 85 | 자녀를 사칭하여 긴급한 상황에서 금전을 요구하는 전형적인 가족 사칭 패턴입니다. |
| 20 | adversarial_compressed | family_impersonation | family_impersonation | 85 | 자녀를 사칭하여 긴급한 상황에서 금전을 요구하는 전형적인 가족 사칭 패턴입니다. |
| 21 | base | benign | benign | 0 | 일상적인 약속 잡기 내용으로 사기 의도가 없음 |
| 22 | base | benign | benign | 0 | 농협 은행에서 보낸 정상적인 거래 내역으로 판단됩니다. |
| 23 | base | benign | benign | 0 | 일상적인 가족 간 대화로 사기 의도가 없음 |
| 24 | base | benign | benign | 0 | 일반적인 택배 배송 완료 알림으로 사기 의도가 없어 보입니다. |
| 25 | base | benign | benign | 0 | 정상적인 개인 간 대화로 사기 의도가 없음 |
