"""매크로 데이터 수집 — FRED, Yahoo Finance."""

import yfinance as yf
from loguru import logger
from config.settings import settings

try:
    from fredapi import Fred
except ImportError:
    logger.warning("fredapi 미설치")


class MacroCollector:
    """미국/한국 매크로 지표 수집."""

    MACRO_TICKERS = {
        "VIX": "^VIX",
        "SP500": "^GSPC",
        "NASDAQ": "^IXIC",
        "DXY": "DX-Y.NYB",
        "USDKRW": "KRW=X",
    }

    FRED_SERIES = {
        "fed_rate": "FEDFUNDS",
        "cpi": "CPIAUCSL",
        "unemployment": "UNRATE",
    }

    def get_yahoo_data(self, ticker: str, period: str = "1y") -> dict:
        """Yahoo Finance 데이터 조회."""
        try:
            data = yf.Ticker(ticker).history(period=period)
            return data.to_dict()
        except Exception as e:
            logger.error(f"Yahoo Finance 조회 실패 ({ticker}): {e}")
            return {}

    def get_fred_data(self, series_id: str) -> dict:
        """FRED API 데이터 조회."""
        try:
            fred = Fred(api_key=settings.fred_api_key)
            data = fred.get_series(series_id)
            return data.to_dict()
        except Exception as e:
            logger.error(f"FRED 조회 실패 ({series_id}): {e}")
            return {}

    async def collect_all(self) -> dict:
        """전체 매크로 지표 수집."""
        result = {}
        for name, ticker in self.MACRO_TICKERS.items():
            result[name] = self.get_yahoo_data(ticker, period="1mo")
        return result
