-- 초기 스키마 마이그레이션
-- TimescaleDB 확장 활성화
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 주가 시계열 테이블
CREATE TABLE IF NOT EXISTS prices (
    time        TIMESTAMPTZ NOT NULL,
    stock_code  VARCHAR(10) NOT NULL,
    open        DOUBLE PRECISION,
    high        DOUBLE PRECISION,
    low         DOUBLE PRECISION,
    close       DOUBLE PRECISION,
    volume      BIGINT,
    PRIMARY KEY (time, stock_code)
);
SELECT create_hypertable('prices', 'time', if_not_exists => TRUE);

-- 매매 이력
CREATE TABLE IF NOT EXISTS trades (
    id                  SERIAL PRIMARY KEY,
    timestamp           TIMESTAMPTZ DEFAULT NOW(),
    stock_code          VARCHAR(10) NOT NULL,
    action              VARCHAR(10) NOT NULL,
    quantity            INTEGER,
    price               DOUBLE PRECISION,
    pnl                 DOUBLE PRECISION DEFAULT 0,
    strategy_name       VARCHAR(100),
    signal_confidence   DOUBLE PRECISION,
    paper_trade         BOOLEAN DEFAULT TRUE
);

-- 전략 메타데이터
CREATE TABLE IF NOT EXISTS strategies (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100) UNIQUE NOT NULL,
    description     TEXT,
    active          BOOLEAN DEFAULT FALSE,
    config_json     JSONB,
    backtest_result JSONB,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- 봇 기억
CREATE TABLE IF NOT EXISTS bot_memory (
    id          SERIAL PRIMARY KEY,
    memory_type VARCHAR(50) NOT NULL,
    content     JSONB,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_bot_memory_type ON bot_memory (memory_type);

-- 뉴스 기사
CREATE TABLE IF NOT EXISTS news_articles (
    id              SERIAL PRIMARY KEY,
    stock_code      VARCHAR(10),
    title           TEXT,
    content         TEXT,
    sentiment       VARCHAR(20),
    sentiment_score DOUBLE PRECISION,
    published_at    TIMESTAMPTZ,
    source          VARCHAR(50),
    collected_at    TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_news_stock ON news_articles (stock_code, published_at DESC);
