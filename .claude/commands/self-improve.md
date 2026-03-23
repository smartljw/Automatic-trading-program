# /self-improve

봇 자기개선 사이클을 수동으로 실행합니다.

## 사용법
```
/self-improve [분석 기간: 7d|30d|90d]
```

## 실행 단계
1. `self_learning/bot_memory.py` 에서 성과 데이터 및 실패 패턴 로드
2. `self_learning/learning_agent.py` Claude API 분석 실행
3. 개선안 출력 (change_type, risk_level, requires_approval)
4. LOW/MEDIUM 리스크 + 승인 불필요 항목 자동 적용
5. HIGH 리스크 또는 승인 필요 항목은 사용자에게 텔레그램 전송

## 규칙
- `config/risk_limits.py` HARD_LIMITS 는 절대 변경 불가
- ML 모델 교체는 반드시 사용자 승인 필요
