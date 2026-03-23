"""퀀트 전략 엔진 테스트."""

import pytest
import pandas as pd
import numpy as np
from strategy.quant_engine import QuantEngine
from strategy.strategy_base import StrategyConfig


@pytest.fixture
def sample_config():
    return StrategyConfig(
        name="테스트_RSI전략",
        description="테스트용",
        active=True,
        stocks=[],
        buy_conditions=[{"indicator": "RSI", "period": 14, "operator": "<", "value": 30}],
        sell_conditions=[{"indicator": "RSI", "period": 14, "operator": ">", "value": 70}],
        position_size=0.10,
    )


@pytest.fixture
def oversold_data():
    """RSI 30 이하 과매도 데이터."""
    np.random.seed(42)
    prices = [100.0]
    for _ in range(30):
        prices.append(prices[-1] * (1 - abs(np.random.normal(0, 0.02))))
    df = pd.DataFrame({
        "종가": prices,
        "거래량": [1_000_000] * len(prices),
    })
    return df


def test_rsi_buy_signal(sample_config, oversold_data):
    engine = QuantEngine(sample_config)
    signal = engine.generate_signal("005930", oversold_data)
    assert signal.stock_code == "005930"
    assert signal.action in ("BUY", "HOLD")  # 데이터에 따라 다름


def test_calc_rsi():
    prices = pd.Series([100, 102, 101, 103, 102, 100, 98, 97, 96, 95,
                        94, 93, 92, 91, 90, 89, 88, 87, 86, 85])
    rsi = QuantEngine._calc_rsi(prices, 14)
    assert len(rsi) == len(prices)
    assert 0 <= rsi.dropna().iloc[-1] <= 100
