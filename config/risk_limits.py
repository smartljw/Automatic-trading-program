"""
리스크 절대 한도 — 이 파일은 AI가 절대 수정하지 않습니다.
CLAUDE.md 규칙: config/risk_limits.py → AI가 절대 수정 불가
"""

# ============================================================
# 하드 리밋 — 어떤 상황에서도 초과 불가
# ============================================================
HARD_LIMITS = {
    "MAX_POSITION_PER_STOCK": 0.25,   # 종목당 최대 비중 25%
    "MAX_DAILY_LOSS": 0.05,            # 하루 최대 손실 5%
    "MAX_DRAWDOWN_STOP": 0.10,         # 고점 대비 -10% → 전략 전면 정지
    "MIN_STOP_LOSS": 0.02,             # 손절 최소 2% (더 타이트하게는 변경 가능, 완화 불가)
    "MAX_STOCKS_HELD": 10,             # 동시 보유 최대 10종목
    "MIN_CONFIDENCE": 0.55,            # AI 확신도 55% 미만 → 관망
    "REQUIRE_BACKTEST_DAYS": 365,      # 전략 등록 시 1년 백테스트 필수
    "MAX_ORDER_PER_DAY": 50,           # 하루 최대 주문 횟수
    "MIN_CASH_RATIO": 0.10,            # 항상 현금 최소 10% 유지
}

# ============================================================
# AI 자동 적용 허용 변경 (더 보수적인 방향만)
# ============================================================
AUTO_APPLY_SAFE = [
    "손절 강화 (더 타이트하게)",
    "매매 횟수 축소",
    "관망 조건 추가",
    "확신도 임계값 상향",
    "포지션 크기 축소",
    "특정 종목 매매 일시 제한",
]

# ============================================================
# 반드시 사용자 승인 필요
# ============================================================
REQUIRE_HUMAN_APPROVAL = [
    "리스크 한도 완화",
    "새 전략 규칙 추가",
    "ML 모델 교체 (production)",
    "새 모듈 시스템 통합",
    "실전 자금 비중 증가",
    "HARD_LIMITS 어떤 항목이든 변경",
]


def check_position_limit(portfolio_value: float, order_value: float, stock_code: str) -> bool:
    """종목 비중 한도 검사."""
    ratio = order_value / portfolio_value
    if ratio > HARD_LIMITS["MAX_POSITION_PER_STOCK"]:
        raise ValueError(
            f"[RISK] {stock_code} 주문 비중 {ratio:.1%} > 한도 {HARD_LIMITS['MAX_POSITION_PER_STOCK']:.1%}"
        )
    return True


def check_daily_loss(daily_pnl: float, portfolio_value: float) -> bool:
    """일일 손실 한도 검사."""
    loss_ratio = daily_pnl / portfolio_value
    if loss_ratio < -HARD_LIMITS["MAX_DAILY_LOSS"]:
        raise ValueError(
            f"[RISK] 일일 손실 {loss_ratio:.1%} > 한도 {HARD_LIMITS['MAX_DAILY_LOSS']:.1%} — 매매 중단"
        )
    return True


def check_drawdown(current_value: float, peak_value: float) -> bool:
    """드로우다운 한도 검사."""
    drawdown = (current_value - peak_value) / peak_value
    if drawdown < -HARD_LIMITS["MAX_DRAWDOWN_STOP"]:
        raise ValueError(
            f"[RISK] 드로우다운 {drawdown:.1%} > 한도 {HARD_LIMITS['MAX_DRAWDOWN_STOP']:.1%} — 전략 정지"
        )
    return True


def check_confidence(confidence: float) -> bool:
    """AI 확신도 검사."""
    if confidence < HARD_LIMITS["MIN_CONFIDENCE"]:
        return False  # 관망
    return True
