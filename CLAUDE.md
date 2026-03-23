# TRADING AI BOT — 완전 기획서 (CLAUDE.md)

> 이 파일을 프로젝트 루트에 저장하면 Claude Code가 매 세션마다 자동으로 읽어요.
> Claude Code에서 "이 기획서대로 Phase 1부터 구현 시작해줘" 라고 입력하면 돼요.

---

## 프로젝트 개요

**프로젝트명**: trading-ai-bot  
**목적**: 개인용 AI 주식 자동매매 봇 — 핸드폰(텔레그램)으로 조작, 스스로 학습하고 성장하는 완전 자율 시스템  
**개발 환경**: Windows WSL2(Ubuntu) + Python 3.11 + Claude Code  
**핵심 철학**: 데이터 수집 → AI 판단 → 자동 실행 → 자가 학습 → 스스로 성장

---

## 전체 시스템 구성 (5개 핵심 모듈)

```
trading-ai-bot/
│
├── CLAUDE.md                        # 이 파일 (Claude Code 컨텍스트)
├── .claude/
│   ├── settings.json                # Claude Code 권한 설정
│   └── commands/
│       ├── new-strategy.md          # /new-strategy 커스텀 명령
│       ├── backtest.md              # /backtest 커스텀 명령
│       ├── deploy.md                # /deploy 커스텀 명령
│       └── self-improve.md         # /self-improve 커스텀 명령
│
├── core/                            # 시스템 두뇌
│   ├── orchestrator.py              # 전체 모듈 조율 (메인 루프)
│   ├── risk_manager.py              # 리스크 관리 (하드 리밋)
│   ├── order_executor.py            # KIS API 주문 실행기
│   └── scheduler.py                 # 작업 스케줄러 (장 시작/종료)
│
├── data/                            # 데이터 수집 파이프라인
│   ├── kis_stream.py                # KIS WebSocket 실시간 시세
│   ├── news_collector.py            # 뉴스/기사 수집 (네이버, DART)
│   ├── financial_collector.py       # 재무제표 수집 (DART OpenAPI)
│   ├── macro_collector.py           # 매크로 데이터 (FRED, Yahoo)
│   ├── chart_collector.py           # 차트/기술적 지표 수집
│   ├── overseas_collector.py        # 해외 뉴스 (Finnhub, NewsAPI)
│   ├── community_collector.py       # 커뮤니티 감성 (네이버 카페 등)
│   └── data_manager.py              # 데이터 통합 관리 + 자동 업데이트
│
├── strategy/                        # 전략 엔진
│   ├── strategy_base.py             # 전략 기본 클래스
│   ├── quant_engine.py              # 수식/조건문 기반 퀀트 전략
│   ├── strategy_store.py            # 전략 생성/저장/활성화 관리
│   └── signal_aggregator.py        # 전략 신호 통합기
│
├── ai/                              # AI 엔진
│   ├── ensemble.py                  # 앙상블 투표기 (퀀트+ML+LLM)
│   ├── ml_predictor.py              # LSTM + XGBoost 예측 모델
│   ├── sentiment_analyzer.py        # FinBERT 감성 분석
│   ├── rl_agent.py                  # 강화학습 에이전트 (PPO)
│   └── model_trainer.py             # 야간 자동 재학습
│
├── self_learning/                   # 자가학습 핵심 모듈
│   ├── learning_agent.py            # Claude API 기반 자기개선 엔진
│   ├── bot_memory.py                # 장기 기억 + 실패 패턴 저장
│   ├── knowledge_base.py            # 학습된 지식 + 인사이트 DB
│   ├── code_generator.py            # 새 모듈/에이전트 자동 생성
│   ├── self_evaluator.py            # 스스로 성과 평가 + 개선안 도출
│   └── feedback_processor.py        # 사용자 피드백 처리 + 반영
│
├── assistant/                       # AI 비서 + 텔레그램 인터페이스
│   ├── telegram_bot.py              # 텔레그램 봇 (핸드폰 조작)
│   ├── claude_agent.py              # Claude API 총괄 LLM
│   ├── chat_handler.py              # 메신저형 채팅 인터페이스
│   └── command_parser.py            # 자연어 명령 → 시스템 명령 변환
│
├── backtest/
│   ├── backtester.py                # 백테스트 엔진
│   ├── performance_analyzer.py      # 성과 분석 (샤프, MDD, 승률)
│   └── report_generator.py          # 백테스트 리포트 생성
│
├── monitoring/
│   ├── dashboard_server.py          # FastAPI 웹 대시보드 서버
│   ├── chart_visualizer.py          # 차트 시각화
│   ├── trade_visualizer.py          # 매매 내역 시각화
│   └── reporter.py                  # 일별/주별 자동 리포트
│
├── db/
│   ├── timescale_client.py          # TimescaleDB 연결 (시계열)
│   ├── models.py                    # DB 스키마 정의
│   └── migrations/                  # DB 마이그레이션
│
├── storage/
│   ├── knowledge_store.py           # AI 학습 데이터 저장 (최적 포맷)
│   ├── model_store.py               # 훈련된 모델 버전 관리
│   └── asset_store.py               # 차트 이미지 등 파일 저장
│
├── config/
│   ├── settings.py                  # 전체 설정 (env 참조)
│   ├── risk_limits.py               # 리스크 절대 한도 (하드코딩)
│   └── strategy_config.yaml         # 활성 전략 목록 + 파라미터
│
├── tests/                           # 자동 테스트
├── scripts/                         # 배포/운영 스크립트
├── .env.example                     # 환경변수 템플릿
├── docker-compose.yml               # DB + 서비스 컨테이너
├── requirements.txt
└── README.md
```

---

## 모듈 1 — 데이터 수집 파이프라인

### 수집 대상 전체 목록

**실시간 (WebSocket/폴링)**
- KIS WebSocket: 체결가, 호가, 거래량 실시간 스트림
- 네이버 금융 실시간: 현재가, 등락률, 거래대금
- DART 공시 RSS: 중요 공시 즉시 감지

**일별 자동 수집 (스케줄러)**
- 재무제표: DART OpenAPI (분기별 실적, PER, PBR, ROE, 부채비율)
- 차트 데이터: pykrx + FinanceDataReader (일봉/주봉/월봉 OHLCV)
- 기술적 지표: RSI, MACD, 볼린저밴드, 이동평균, 거래량 지표 자동 계산
- 외국인/기관 순매수: KIS API + pykrx
- 공매도 현황: KRX 데이터
- 업종별 등락: KIS API

**뉴스/감성 (30분 간격)**
- 네이버 뉴스 API: 종목명 검색 → 최신 기사 수집
- DART 공시: 실적발표, 배당, 유상증자 등
- Finnhub: 영문 글로벌 뉴스 + 시장 감성 지수
- 관련주 탐색: 동일 업종/테마 종목 연동

**매크로 (일 1회)**
- FRED API: 미국 금리, CPI, 실업률
- Yahoo Finance: VIX, S&P500, 나스닥, 달러인덱스, 환율
- 한국은행 ECOS API: 국내 금리, 통화량

**빅데이터 / AI 학습용**
- 과거 5년 주가 데이터 + 기술적 지표 (모델 학습용)
- 전체 매매 이력 → 성공/실패 패턴 자동 레이블링
- 뉴스-주가 상관관계 데이터셋 자동 구축
- 데이터 최적 저장: Parquet 포맷 (빠른 읽기), 차트는 PNG

### 데이터 자동 업데이트 규칙
```python
# config/settings.py 에 정의
DATA_UPDATE_SCHEDULE = {
    "realtime": ["price", "orderbook"],           # 실시간
    "every_30min": ["news", "dart_rss"],          # 30분
    "daily_9am": ["financials", "indicators"],    # 장 시작 전
    "daily_6pm": ["charts", "foreign_flow"],      # 장 마감 후
    "weekly": ["macro", "sector_analysis"],       # 주 1회
}
```

---

## 모듈 2 — 전략 엔진

### 퀀트 전략 생성 시스템
사용자가 수식/조건문으로 전략을 직접 만들고 저장할 수 있어야 함.

```python
# 전략 예시 구조 (strategy_store.py)
strategy = {
    "name": "RSI_역추세_전략",
    "description": "RSI 30 이하 과매도 구간 매수",
    "active": True,
    "stocks": ["005930", "000660"],  # 적용 종목
    "buy_conditions": [
        {"indicator": "RSI", "period": 14, "operator": "<", "value": 30},
        {"indicator": "VOLUME", "operator": ">", "value": "MA_20_volume * 1.5"},
    ],
    "sell_conditions": [
        {"indicator": "RSI", "period": 14, "operator": ">", "value": 70},
        {"type": "stop_loss", "value": -0.05},
        {"type": "take_profit", "value": 0.10},
    ],
    "position_size": 0.10,  # 계좌의 10%
    "created_at": "2024-01-01",
    "backtest_result": None,  # 생성 시 자동 백테스트 실행
}
```

### 지원할 기술적 지표 (quant_engine.py)
RSI, MACD, 볼린저밴드, 이동평균(5/10/20/60/120일), 스토캐스틱,
ATR, OBV, 거래량 지표, 캔들 패턴, 신고가/신저가, 괴리율

### 앙상블 신호 (3개 모델 가중 투표)
1. 퀀트 모델 (가중치 0.40): 기술적 지표 기반 규칙
2. ML 예측 모델 (가중치 0.35): LSTM + XGBoost 방향 예측
3. LLM 감성 분석 (가중치 0.25): FinBERT 뉴스 감성 → 신호
- 최종 점수 > 0.65: 매수 / < 0.35: 매도 / 그 외: 관망
- 가중치는 최근 90일 성과 기반 자동 조정

---

## 모듈 3 — 자가학습 AI 봇 (핵심)

### 자가학습 3단계

**레벨 A — 파라미터 자동 조정** (즉시 적용)
- 손절 비율, 매매 비중, 신호 임계값 자동 최적화
- 성과 데이터 기반 → Claude API가 분석 → config 업데이트

**레벨 B — 전략 규칙 자동 추가/수정** (백테스트 후 적용)
- Claude API가 새 조건문 코드 생성
- 1년 백테스트 통과 시 strategy_config.yaml에 등록

**레벨C — ML 모델 자동 재학습** (야간 배치)
- 최신 데이터로 LSTM, XGBoost 모델 업데이트
- 성과가 향상된 모델만 production 교체

**레벨 D — 새 모듈/에이전트 자동 생성** (고도화)
- Claude API가 스스로 필요한 기능 파악
- 코드 생성 → 테스트 → 통과 시 시스템에 통합
- 예: "해외선물 데이터 수집 필요" → 새 collector 모듈 자동 생성

### 자기학습 핵심 프롬프트 구조 (learning_agent.py)
```python
SELF_LEARNING_SYSTEM_PROMPT = """
너는 trading-ai-bot의 자기개선 엔진이야.
주어진 성과 데이터와 실패 패턴을 분석해서
구체적인 개선안을 JSON으로만 응답해.

응답 형식:
{
  "analysis": "현재 문제점 분석",
  "change_type": "PARAM | RULE | RETRAIN | NEW_MODULE",
  "changes": [...],
  "expected_impact": "예상 효과",
  "risk_level": "LOW | MEDIUM | HIGH",
  "requires_approval": true/false
}

절대 불변 규칙:
- 종목당 최대 비중 25% 초과 불가
- 일일 손실 한도 5% 초과 완화 불가
- 드로우다운 10% 초과 시 전략 정지는 제거 불가
"""
```

### 봇 메모리 구조 (bot_memory.py)
```python
# 저장되는 기억 유형
MEMORY_TYPES = {
    "trade_history": "전체 매매 이력 (진입/청산/손익)",
    "failure_patterns": "손실 매매 패턴 분석",
    "success_patterns": "수익 매매 패턴 분석",
    "market_insights": "시장 국면별 전략 성과",
    "news_impact": "뉴스 종류 → 주가 영향 상관관계",
    "user_feedback": "사용자가 전달한 피드백 이력",
    "code_changes": "자동 변경된 코드 이력",
    "model_versions": "ML 모델 버전별 성과 이력",
}
```

---

## 모듈 4 — 텔레그램 봇 (핸드폰 조작 인터페이스)

### 명령어 체계

**빠른 조작 명령어**
```
/status          현재 포트폴리오 + 오늘 수익률
/positions       보유 종목 목록
/pause           전략 일시 정지
/resume          전략 재개
/emergency       전체 포지션 즉시 청산
/report          오늘 매매 요약 리포트
/watchlist       관심 종목 목록
/add_watch 종목  관심 종목 추가
```

**전략 관리**
```
/strategies      활성화된 전략 목록
/activate 전략명 전략 활성화
/deactivate 전략명 전략 비활성화
/backtest 전략명 백테스트 실행 후 결과 전송
```

**자연어 명령 (Claude API 처리)**
```
"삼성전자 10주 매수해줘"
"오늘 왜 손실 났어? 분석해줘"
"손절을 3%로 타이트하게 바꿔줘"
"공시 뜨면 무조건 10분 관망하는 규칙 추가해줘"
"이번 달 성과 요약해줘"
"반도체 업종 요즘 어때?"
"스스로 가장 고쳐야 할 점 찾아봐"
"새로운 전략 하나 만들어줘 — RSI + 거래량 급증 조합으로"
```

**AI 봇 성장 명령**
```
"이러이러한 점을 통해 스스로 학습하고 보완해줘"
"최근 실패 패턴 분석해서 전략 개선해줘"
"지금 시장에 맞는 전략으로 자동 조정해줘"
"새로운 데이터 소스가 필요하면 스스로 추가해줘"
```

### 메신저형 채팅 인터페이스
- 텔레그램 채팅창이 AI 비서와의 대화 창구
- 일반 대화 → Claude API가 의도 파악 → 시스템 명령으로 변환
- 매매 발생 시 자동 알림 (매수/매도 체결, 손절 발동 등)
- 일별 성과 리포트 자동 전송 (오후 6시)

---

## 모듈 5 — 웹 대시보드 (FastAPI + 모바일 최적화)

### 주요 화면 구성

**메인 대시보드**
- 계좌 요약 (총 자산, 오늘 손익, 수익률 그래프)
- 활성 전략 현황 카드
- 실시간 보유 종목 현황
- AI 봇 상태 표시 (학습 중 / 매매 대기 / 실행 중)

**차트 & 시각화**
- 종목별 캔들 차트 + 기술적 지표 오버레이
- 매수/매도 포인트 차트에 표시
- 수익률 곡선 그래프
- 전략별 성과 비교 차트
- 드로우다운 차트

**전략 관리 UI**
- 전략 목록 + 활성화 토글
- 새 전략 생성 폼 (수식/조건문 입력)
- 백테스트 결과 시각화

**AI 학습 현황**
- 학습 데이터 현황 (수집된 데이터 양)
- 모델 성능 지표 추이
- 최근 자동 변경 이력
- 다음 재학습 예정 시간

**매매 이력**
- 전체 매매 내역 테이블
- 성공/실패 분류 + 원인 분석
- 관심 종목 관리

---

## 리스크 관리 절대 한도 (코드에서 변경 불가)

```python
# config/risk_limits.py — 이 파일은 AI가 수정 불가
HARD_LIMITS = {
    "MAX_POSITION_PER_STOCK": 0.25,    # 종목당 최대 25%
    "MAX_DAILY_LOSS": 0.05,            # 하루 최대 손실 5%
    "MAX_DRAWDOWN_STOP": 0.10,         # 고점 대비 -10% → 전략 정지
    "MIN_STOP_LOSS": 0.02,             # 손절 최소 2% (더 타이트하게 못 바꿈)
    "MAX_STOCKS_HELD": 10,             # 동시 보유 최대 10종목
    "MIN_CONFIDENCE": 0.55,            # AI 확신도 55% 미만 → 관망
    "REQUIRE_BACKTEST_DAYS": 365,      # 전략 추가 시 1년 백테스트 필수
}

# AI가 자동 적용 가능한 변경 (더 보수적인 방향만)
AUTO_APPLY_SAFE = [
    "손절 강화 (더 타이트하게)",
    "매매 횟수 축소",
    "관망 조건 추가",
    "확신도 임계값 상향",
]

# 반드시 사용자 승인 필요
REQUIRE_HUMAN_APPROVAL = [
    "리스크 한도 완화",
    "새 전략 규칙 추가",
    "ML 모델 교체",
    "새 모듈 시스템 통합",
    "실전 자금 비중 증가",
]
```

---

## 기술 스택 전체 목록

**백엔드 / 코어**
- Python 3.11
- FastAPI (웹 대시보드 API 서버)
- APScheduler (작업 스케줄러)
- asyncio + aiohttp (비동기 처리)

**데이터베이스**
- TimescaleDB (시계열 주가/지표 데이터)
- PostgreSQL (매매 이력, 전략, 설정)
- Redis (실시간 캐시, 세션)

**AI / ML**
- PyTorch (LSTM 모델)
- scikit-learn + XGBoost (특징 기반 예측)
- transformers + FinBERT (뉴스 감성 분석)
- stable-baselines3 (강화학습 PPO)
- Anthropic Claude API (LLM 비서 + 자가학습)

**데이터 수집**
- KIS REST API + WebSocket (한국투자증권)
- pykrx (KRX 데이터)
- FinanceDataReader (주가 히스토리)
- DART OpenAPI (공시/재무제표)
- 네이버 뉴스 API
- Finnhub API (글로벌 뉴스)
- FRED API (미국 매크로)
- Yahoo Finance / yfinance

**프론트엔드 (웹 대시보드)**
- React + TypeScript
- TradingView Lightweight Charts (캔들 차트)
- Recharts (성과 그래프)
- Tailwind CSS (모바일 반응형)

**인프라**
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- AWS EC2 또는 GCP (클라우드 배포, 24시간 운용)

**외부 서비스**
- Telegram Bot API (모바일 조작 인터페이스)

---

## 개발 단계별 계획

### Phase 1 (1~2개월) — 핵심 기반 구축
- [ ] 프로젝트 폴더 구조 + Docker 환경 세팅
- [ ] KIS REST API 연동 (인증, 시세 조회, 주문 실행)
- [ ] KIS WebSocket 실시간 시세 수신
- [ ] TimescaleDB + PostgreSQL 스키마 설계
- [ ] 퀀트 전략 엔진 기초 (RSI, MACD, 볼린저밴드)
- [ ] 전략 생성/저장/활성화 시스템
- [ ] 백테스트 엔진 (1년 데이터 기반)
- [ ] 리스크 관리 모듈 (손절, 비중 제한)
- [ ] 텔레그램 봇 기본 명령어 (/status, /pause, /report)
- [ ] 모의투자 모드 전체 테스트

### Phase 2 (3~4개월) — 데이터 파이프라인 + AI 엔진
- [ ] 전체 데이터 수집 파이프라인 완성
- [ ] pykrx + DART + 네이버 뉴스 자동 수집
- [ ] FinBERT 감성 분석 모듈
- [ ] LSTM + XGBoost 예측 모델 학습
- [ ] 앙상블 투표기 완성
- [ ] Claude API 기반 AI 비서 기초
- [ ] 자연어 명령 → 시스템 명령 변환
- [ ] 웹 대시보드 기초 (포트폴리오 현황)
- [ ] 차트 시각화 (캔들 + 매매 포인트)

### Phase 3 (5~6개월) — 자가학습 시스템 + 고도화
- [ ] 봇 메모리 + 지식베이스 구현
- [ ] 자가학습 에이전트 완성 (레벨 A~C)
- [ ] 실패 패턴 자동 분석 + 피드백 반영
- [ ] 새 모듈 자동 생성 기능 (레벨 D)
- [ ] 메신저형 채팅 인터페이스 완성
- [ ] 웹 대시보드 전체 완성 (모바일 최적화)
- [ ] 일별/주별 자동 리포트
- [ ] AWS 배포 + 24시간 무중단 운용

### Phase 4 (7개월~) — 실전 + 강화학습
- [ ] 소액 실전 투입 (10만원부터 시작)
- [ ] 강화학습 에이전트 시뮬레이션
- [ ] 전략 성과 기반 가중치 자동 조정
- [ ] 점진적 실전 비중 확대
- [ ] 완전 자율 매매 시스템 완성

---

## Claude Code 작업 규칙

### 코딩 원칙
1. 모든 API 키는 `.env` 파일에서만 로드 (하드코딩 절대 금지)
2. 주문 실행 전 반드시 `PAPER_TRADE` 환경변수 확인
3. 리스크 한도 초과 시 주문 거부 로직 모든 주문 함수에 포함
4. 모든 매매 행위 TimescaleDB에 즉시 로깅
5. 에러 발생 시 텔레그램으로 즉시 알림 발송
6. 새 기능 추가 시 반드시 테스트 코드 함께 작성
7. 작업 단위마다 git commit (커밋 메시지 자동 생성)

### 파일 작업 시 주의사항
- `config/risk_limits.py` → AI가 절대 수정 불가
- `.env` 파일 → git에 절대 포함 금지
- `core/order_executor.py` → 변경 시 반드시 모의투자 테스트 먼저

### 테스트 기준
- 전략 추가: 1년 백테스트 샤프비율 > 0.8 통과 시만 등록
- ML 모델 교체: 검증 데이터 정확도 이전 모델 이상일 때만 교체
- 새 데이터 소스: 30일 수집 안정성 확인 후 정식 등록

---

## 환경변수 목록 (.env.example)

```
# 한국투자증권 KIS API
KIS_APP_KEY=your_app_key
KIS_APP_SECRET=your_app_secret
KIS_ACCOUNT_NO=your_account_number
KIS_PAPER_TRADE=true  # 모의투자: true, 실전: false

# Anthropic Claude API
ANTHROPIC_API_KEY=your_claude_api_key

# 텔레그램
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# 데이터 수집 API
DART_API_KEY=your_dart_key
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_secret
FINNHUB_API_KEY=your_finnhub_key
FRED_API_KEY=your_fred_key

# 데이터베이스
TIMESCALE_URL=postgresql://user:pass@localhost:5432/trading
REDIS_URL=redis://localhost:6379

# 서버
DASHBOARD_PORT=8000
SECRET_KEY=your_secret_key
```