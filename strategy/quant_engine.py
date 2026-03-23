"""수식/조건문 기반 퀀트 전략 엔진."""

import pandas as pd
import numpy as np
from loguru import logger
from strategy.strategy_base import StrategyBase, StrategyConfig, Signal


class QuantEngine(StrategyBase):
    """RSI, MACD, 볼린저밴드 등 기술적 지표 기반 규칙 전략."""

    SUPPORTED_INDICATORS = [
        "RSI", "MACD", "BOLLINGER", "MA", "MA_CROSS",
        "STOCHASTIC", "ATR", "OBV", "VOLUME",
        "NEW_HIGH", "NEW_LOW",
    ]

    def generate_signal(self, stock_code: str, data: pd.DataFrame) -> Signal:
        """조건문 목록을 평가해 매매 신호 생성."""
        if not self.is_applicable(stock_code):
            return Signal(stock_code, "HOLD", 0.0, self.config.name)

        buy_score = self._evaluate_conditions(data, self.config.buy_conditions)
        sell_score = self._evaluate_conditions(data, self.config.sell_conditions)

        if sell_score == 1.0:
            return Signal(stock_code, "SELL", sell_score, self.config.name, "매도 조건 충족")
        elif buy_score == 1.0:
            return Signal(stock_code, "BUY", buy_score, self.config.name, "매수 조건 충족")
        else:
            return Signal(stock_code, "HOLD", 0.5, self.config.name, "조건 미충족")

    def _evaluate_conditions(self, data: pd.DataFrame, conditions: list[dict]) -> float:
        """조건 목록 평가 — 모두 충족 시 1.0, 미충족 시 0.0."""
        if not conditions:
            return 0.0
        results = [self._check_condition(data, cond) for cond in conditions]
        return 1.0 if all(results) else 0.0

    def _check_condition(self, data: pd.DataFrame, condition: dict) -> bool:
        """단일 조건 평가."""
        cond_type = condition.get("type")
        indicator = condition.get("indicator")

        if cond_type == "stop_loss":
            return False  # 손절은 별도 처리

        if cond_type == "take_profit":
            return False  # 익절은 별도 처리

        if indicator == "RSI":
            return self._check_rsi(data, condition)
        elif indicator == "VOLUME":
            return self._check_volume(data, condition)
        elif indicator == "MA_CROSS":
            return self._check_ma_cross(data, condition)

        logger.warning(f"지원하지 않는 지표: {indicator}")
        return False

    def _check_rsi(self, data: pd.DataFrame, condition: dict) -> bool:
        period = condition.get("period", 14)
        operator = condition.get("operator")
        value = condition.get("value")
        rsi = self._calc_rsi(data["종가"], period)
        if operator == "<":
            return rsi.iloc[-1] < value
        elif operator == ">":
            return rsi.iloc[-1] > value
        return False

    def _check_volume(self, data: pd.DataFrame, condition: dict) -> bool:
        latest_vol = data["거래량"].iloc[-1]
        threshold = data["거래량"].rolling(20).mean().iloc[-1] * 1.5
        if condition.get("operator") == ">":
            return latest_vol > threshold
        return False

    def _check_ma_cross(self, data: pd.DataFrame, condition: dict) -> bool:
        fast = condition.get("fast", 5)
        slow = condition.get("slow", 20)
        direction = condition.get("direction", "golden")
        ma_fast = data["종가"].rolling(fast).mean()
        ma_slow = data["종가"].rolling(slow).mean()
        if direction == "golden":
            return ma_fast.iloc[-1] > ma_slow.iloc[-1] and ma_fast.iloc[-2] <= ma_slow.iloc[-2]
        elif direction == "dead":
            return ma_fast.iloc[-1] < ma_slow.iloc[-1] and ma_fast.iloc[-2] >= ma_slow.iloc[-2]
        return False

    @staticmethod
    def _calc_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        delta = prices.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(com=period - 1, adjust=False).mean()
        avg_loss = loss.ewm(com=period - 1, adjust=False).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
