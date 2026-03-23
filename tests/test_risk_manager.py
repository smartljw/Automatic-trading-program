"""리스크 관리 모듈 테스트."""

import pytest
from core.risk_manager import RiskManager
from config.risk_limits import HARD_LIMITS


def test_position_limit_exceeded():
    rm = RiskManager()
    rm.update_portfolio(10_000_000, 0)
    # 종목당 최대 25% = 2,500,000원 — 초과 금액 주문은 거부
    result = rm.validate_order("005930", 3_000_000, 10_000_000, confidence=0.8)
    assert result is False


def test_position_limit_ok():
    rm = RiskManager()
    rm.update_portfolio(10_000_000, 0)
    result = rm.validate_order("005930", 2_000_000, 10_000_000, confidence=0.8)
    assert result is True


def test_low_confidence_rejected():
    rm = RiskManager()
    rm.update_portfolio(10_000_000, 0)
    result = rm.validate_order("005930", 500_000, 10_000_000, confidence=0.4)
    assert result is False


def test_daily_loss_limit():
    rm = RiskManager()
    # 5% 손실 초과 시 주문 거부
    rm.update_portfolio(10_000_000, -600_000)  # -6%
    result = rm.validate_order("005930", 500_000, 10_000_000, confidence=0.8)
    assert result is False
