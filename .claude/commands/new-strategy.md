# /new-strategy

새로운 퀀트 전략을 생성합니다.

## 사용법
```
/new-strategy [전략 설명]
```

## 실행 단계
1. 사용자 설명을 바탕으로 `strategy/strategy_store.py` 에 새 전략 구성 생성
2. `backtest/backtester.py` 로 1년 백테스트 자동 실행
3. 샤프비율 > 0.8 통과 시 `config/strategy_config.yaml` 에 등록
4. 텔레그램으로 백테스트 결과 전송

## 주의사항
- 모든 전략은 1년 백테스트 필수 (`REQUIRE_BACKTEST_DAYS = 365`)
- 리스크 한도 (`config/risk_limits.py`) 는 절대 수정 금지
