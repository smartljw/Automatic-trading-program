"""전체 시스템 설정 — .env 파일에서 환경변수를 읽어옴."""

import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # KIS API
    kis_app_key: str = Field(..., env="KIS_APP_KEY")
    kis_app_secret: str = Field(..., env="KIS_APP_SECRET")
    kis_account_no: str = Field(..., env="KIS_ACCOUNT_NO")
    kis_paper_trade: bool = Field(True, env="KIS_PAPER_TRADE")
    kis_base_url: str = Field("https://openapivts.koreainvestment.com:29443", env="KIS_BASE_URL")
    kis_ws_url: str = Field("ws://ops.koreainvestment.com:21000", env="KIS_WS_URL")

    # Anthropic
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    claude_model: str = Field("claude-sonnet-4-6", env="CLAUDE_MODEL")

    # 텔레그램
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: str = Field(..., env="TELEGRAM_CHAT_ID")

    # 데이터 수집 API
    dart_api_key: str = Field("", env="DART_API_KEY")
    naver_client_id: str = Field("", env="NAVER_CLIENT_ID")
    naver_client_secret: str = Field("", env="NAVER_CLIENT_SECRET")
    finnhub_api_key: str = Field("", env="FINNHUB_API_KEY")
    fred_api_key: str = Field("", env="FRED_API_KEY")

    # 데이터베이스
    timescale_url: str = Field(..., env="TIMESCALE_URL")
    redis_url: str = Field("redis://localhost:6379", env="REDIS_URL")

    # 서버
    dashboard_port: int = Field(8000, env="DASHBOARD_PORT")
    secret_key: str = Field(..., env="SECRET_KEY")
    allowed_origins: str = Field("http://localhost:3000", env="ALLOWED_ORIGINS")

    # 운영
    log_level: str = Field("INFO", env="LOG_LEVEL")
    timezone: str = Field("Asia/Seoul", env="TIMEZONE")
    model_path: str = Field("./models", env="MODEL_PATH")
    data_path: str = Field("./storage_files", env="DATA_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 데이터 업데이트 스케줄
DATA_UPDATE_SCHEDULE = {
    "realtime": ["price", "orderbook"],
    "every_30min": ["news", "dart_rss"],
    "daily_9am": ["financials", "indicators"],
    "daily_6pm": ["charts", "foreign_flow"],
    "weekly": ["macro", "sector_analysis"],
}

# 앙상블 모델 기본 가중치
ENSEMBLE_WEIGHTS = {
    "quant": 0.40,
    "ml": 0.35,
    "llm": 0.25,
}

# 매매 신호 임계값
SIGNAL_THRESHOLDS = {
    "buy": 0.65,
    "sell": 0.35,
}


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
