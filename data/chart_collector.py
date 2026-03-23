"""차트/기술적 지표 수집 — pykrx + FinanceDataReader."""

import pandas as pd
from datetime import datetime, timedelta
from loguru import logger

try:
    from pykrx import stock as krx
    import FinanceDataReader as fdr
except ImportError:
    logger.warning("pykrx 또는 FinanceDataReader 미설치")


class ChartCollector:
    """OHLCV 차트 데이터 및 기술적 지표를 수집."""

    async def get_ohlcv(
        self,
        stock_code: str,
        start: str,
        end: str,
        period: str = "D",  # D=일봉, W=주봉, M=월봉
    ) -> pd.DataFrame:
        """pykrx로 OHLCV 데이터 조회."""
        try:
            df = krx.get_market_ohlcv(start, end, stock_code)
            return df
        except Exception as e:
            logger.error(f"OHLCV 조회 실패 ({stock_code}): {e}")
            return pd.DataFrame()

    async def get_foreign_institution_flow(self, stock_code: str, start: str, end: str) -> pd.DataFrame:
        """외국인/기관 순매수 데이터."""
        try:
            df = krx.get_market_trading_value_by_date(start, end, stock_code)
            return df
        except Exception as e:
            logger.error(f"외국인/기관 조회 실패: {e}")
            return pd.DataFrame()

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """RSI, MACD, 볼린저밴드 등 기술적 지표 자동 계산."""
        import ta
        df = ta.add_all_ta_features(
            df, open="시가", high="고가", low="저가", close="종가", volume="거래량",
            fillna=True,
        )
        return df
