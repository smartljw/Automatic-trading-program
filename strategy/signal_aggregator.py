"""전략 신호 통합기 — 앙상블 투표."""

from loguru import logger
from strategy.strategy_base import Signal
from config.settings import SIGNAL_THRESHOLDS, ENSEMBLE_WEIGHTS


class SignalAggregator:
    """퀀트/ML/LLM 3개 모델 신호를 가중 평균으로 통합."""

    def aggregate(
        self,
        quant_signal: Signal,
        ml_signal: Signal,
        llm_signal: Signal,
        weights: dict | None = None,
    ) -> Signal:
        """가중 투표로 최종 신호 결정."""
        w = weights or ENSEMBLE_WEIGHTS

        score = (
            self._signal_to_score(quant_signal) * w["quant"]
            + self._signal_to_score(ml_signal) * w["ml"]
            + self._signal_to_score(llm_signal) * w["llm"]
        )

        if score >= SIGNAL_THRESHOLDS["buy"]:
            action = "BUY"
        elif score <= SIGNAL_THRESHOLDS["sell"]:
            action = "SELL"
        else:
            action = "HOLD"

        return Signal(
            stock_code=quant_signal.stock_code,
            action=action,
            confidence=score,
            strategy_name="ensemble",
            reason=f"앙상블 점수: {score:.3f} (Q={quant_signal.confidence:.2f}, ML={ml_signal.confidence:.2f}, LLM={llm_signal.confidence:.2f})",
        )

    @staticmethod
    def _signal_to_score(signal: Signal) -> float:
        """신호를 0~1 점수로 변환."""
        if signal.action == "BUY":
            return signal.confidence
        elif signal.action == "SELL":
            return 1.0 - signal.confidence
        else:
            return 0.5
