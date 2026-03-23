"""전략 기본 클래스."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import pandas as pd


@dataclass
class Signal:
    """매매 신호."""
    stock_code: str
    action: str          # "BUY" | "SELL" | "HOLD"
    confidence: float    # 0.0 ~ 1.0
    strategy_name: str
    reason: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class StrategyConfig:
    """전략 설정 데이터."""
    name: str
    description: str
    active: bool
    stocks: list[str]
    buy_conditions: list[dict]
    sell_conditions: list[dict]
    position_size: float        # 계좌 대비 비중
    created_at: datetime = field(default_factory=datetime.now)
    backtest_result: Optional[dict] = None


class StrategyBase(ABC):
    """모든 전략의 기본 클래스."""

    def __init__(self, config: StrategyConfig):
        self.config = config

    @abstractmethod
    def generate_signal(self, stock_code: str, data: pd.DataFrame) -> Signal:
        """주어진 데이터로 매매 신호 생성."""
        pass

    def is_applicable(self, stock_code: str) -> bool:
        """이 전략이 해당 종목에 적용 가능한지 확인."""
        if not self.config.stocks:  # 빈 리스트 = 전체 적용
            return True
        return stock_code in self.config.stocks
