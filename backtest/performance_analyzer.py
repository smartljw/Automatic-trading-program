"""성과 분석 — 샤프비율, MDD, 승률."""

import numpy as np
import pandas as pd
from backtest.backtester import BacktestResult


class PerformanceAnalyzer:
    """백테스트 결과로 다양한 성과 지표를 계산."""

    @staticmethod
    def sharpe_ratio(returns: list[float], risk_free_rate: float = 0.035) -> float:
        """연환산 샤프비율."""
        if not returns:
            return 0.0
        r = np.array(returns)
        excess = r - risk_free_rate / 252
        if excess.std() == 0:
            return 0.0
        return float(np.sqrt(252) * excess.mean() / excess.std())

    @staticmethod
    def max_drawdown(equity_curve: list[float]) -> float:
        """최대 낙폭(MDD)."""
        if not equity_curve:
            return 0.0
        curve = np.array(equity_curve)
        peak = np.maximum.accumulate(curve)
        drawdown = (curve - peak) / peak
        return float(drawdown.min())

    @staticmethod
    def win_rate(trades: list[dict]) -> float:
        """승률."""
        if not trades:
            return 0.0
        wins = sum(1 for t in trades if t.get("pnl", 0) > 0)
        return wins / len(trades)

    def analyze(self, result: BacktestResult, daily_returns: list[float]) -> BacktestResult:
        """전체 성과 지표 계산 후 결과 업데이트."""
        result.sharpe_ratio = self.sharpe_ratio(daily_returns)
        result.max_drawdown = self.max_drawdown(result.equity_curve)
        return result
