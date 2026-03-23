"""리스크 관리 — 하드 리밋 강제 적용."""

from loguru import logger
from config.risk_limits import (
    HARD_LIMITS,
    check_position_limit,
    check_daily_loss,
    check_drawdown,
    check_confidence,
)


class RiskManager:
    """모든 주문 전 리스크 한도를 검사하는 게이트키퍼."""

    def __init__(self):
        self._peak_value: float = 0.0
        self._daily_pnl: float = 0.0
        self._held_stocks: set = set()

    def validate_order(
        self,
        stock_code: str,
        order_value: float,
        portfolio_value: float,
        confidence: float,
    ) -> bool:
        """주문 전 모든 리스크 조건 검사. 하나라도 실패하면 False 반환."""
        try:
            # 1. AI 확신도 검사
            if not check_confidence(confidence):
                logger.info(f"[RISK] {stock_code} 확신도 {confidence:.2f} 미달 → 관망")
                return False

            # 2. 종목 비중 검사
            check_position_limit(portfolio_value, order_value, stock_code)

            # 3. 일일 손실 검사
            check_daily_loss(self._daily_pnl, portfolio_value)

            # 4. 드로우다운 검사
            check_drawdown(portfolio_value, self._peak_value)

            # 5. 보유 종목 수 검사
            if len(self._held_stocks) >= HARD_LIMITS["MAX_STOCKS_HELD"]:
                if stock_code not in self._held_stocks:
                    logger.warning(f"[RISK] 최대 보유 종목 수 초과 ({HARD_LIMITS['MAX_STOCKS_HELD']}개)")
                    return False

            return True

        except ValueError as e:
            logger.error(str(e))
            return False

    def update_portfolio(self, portfolio_value: float, daily_pnl: float):
        """포트폴리오 상태 업데이트."""
        self._daily_pnl = daily_pnl
        if portfolio_value > self._peak_value:
            self._peak_value = portfolio_value

    def reset_daily(self):
        """장 시작 시 일일 집계 초기화."""
        self._daily_pnl = 0.0
        logger.info("일일 리스크 집계 초기화")
