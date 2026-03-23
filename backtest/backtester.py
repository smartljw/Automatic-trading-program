"""백테스트 엔진."""

import pandas as pd
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger
from config.risk_limits import HARD_LIMITS


@dataclass
class BacktestResult:
    strategy_name: str
    start_date: str
    end_date: str
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    equity_curve: list[float] = field(default_factory=list)


class Backtester:
    """1년 이상 과거 데이터로 전략 성과를 시뮬레이션."""

    INITIAL_CAPITAL = 10_000_000  # 1천만원

    def run(
        self,
        strategy,
        ohlcv_data: dict[str, pd.DataFrame],
        start_date: str,
        end_date: str,
    ) -> BacktestResult:
        """백테스트 실행."""
        logger.info(f"백테스트 시작: {strategy.config.name} ({start_date} ~ {end_date})")

        capital = self.INITIAL_CAPITAL
        positions: dict[str, int] = {}
        trades = []
        equity_curve = [capital]
        peak = capital

        # TODO: 날짜별 시뮬레이션 루프 구현

        result = BacktestResult(
            strategy_name=strategy.config.name,
            start_date=start_date,
            end_date=end_date,
            total_return=(capital - self.INITIAL_CAPITAL) / self.INITIAL_CAPITAL,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            win_rate=0.0,
            total_trades=len(trades),
            equity_curve=equity_curve,
        )
        logger.info(f"백테스트 완료: 수익률={result.total_return:.1%}, 샤프={result.sharpe_ratio:.2f}")
        return result

    def meets_requirements(self, result: BacktestResult) -> bool:
        """전략 등록 기준 충족 여부 (샤프비율 > 0.8)."""
        return result.sharpe_ratio > 0.8
