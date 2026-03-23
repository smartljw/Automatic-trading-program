# /backtest

전략 백테스트를 실행합니다.

## 사용법
```
/backtest [전략명] [시작일] [종료일]
```

## 실행 단계
1. `strategy/strategy_store.py` 에서 전략 로드
2. `data/chart_collector.py` 로 해당 기간 데이터 수집
3. `backtest/backtester.py` 백테스트 실행
4. `backtest/performance_analyzer.py` 성과 지표 계산
5. `backtest/report_generator.py` 리포트 생성 및 출력
