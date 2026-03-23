"""앙상블 투표기 — 퀀트 + ML + LLM 통합."""

import pandas as pd
from loguru import logger
from strategy.strategy_base import Signal
from strategy.signal_aggregator import SignalAggregator


class EnsembleEngine:
    """3개 모델을 조합해 최종 매매 신호를 생성."""

    def __init__(self):
        self.aggregator = SignalAggregator()
        self._weights = {"quant": 0.40, "ml": 0.35, "llm": 0.25}

    async def get_signal(self, stock_code: str, data: pd.DataFrame, news: list[dict]) -> Signal:
        """종목별 앙상블 신호 생성."""
        from ai.ml_predictor import MLPredictor
        from ai.sentiment_analyzer import SentimentAnalyzer
        from strategy.quant_engine import QuantEngine

        quant_signal = await self._get_quant_signal(stock_code, data)
        ml_signal = await self._get_ml_signal(stock_code, data)
        llm_signal = await self._get_llm_signal(stock_code, news)

        return self.aggregator.aggregate(quant_signal, ml_signal, llm_signal, self._weights)

    async def _get_quant_signal(self, stock_code: str, data: pd.DataFrame) -> Signal:
        # TODO: 활성화된 퀀트 전략 실행
        return Signal(stock_code, "HOLD", 0.5, "quant")

    async def _get_ml_signal(self, stock_code: str, data: pd.DataFrame) -> Signal:
        # TODO: LSTM + XGBoost 예측
        return Signal(stock_code, "HOLD", 0.5, "ml")

    async def _get_llm_signal(self, stock_code: str, news: list[dict]) -> Signal:
        # TODO: FinBERT 감성 분석
        return Signal(stock_code, "HOLD", 0.5, "llm")

    def update_weights(self, new_weights: dict):
        """성과 기반 가중치 업데이트 (90일 주기)."""
        total = sum(new_weights.values())
        self._weights = {k: v / total for k, v in new_weights.items()}
        logger.info(f"앙상블 가중치 업데이트: {self._weights}")
