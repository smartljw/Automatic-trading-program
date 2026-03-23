"""봇 장기 기억 + 실패 패턴 저장."""

from datetime import datetime
from loguru import logger

MEMORY_TYPES = {
    "trade_history": "전체 매매 이력 (진입/청산/손익)",
    "failure_patterns": "손실 매매 패턴 분석",
    "success_patterns": "수익 매매 패턴 분석",
    "market_insights": "시장 국면별 전략 성과",
    "news_impact": "뉴스 종류 → 주가 영향 상관관계",
    "user_feedback": "사용자가 전달한 피드백 이력",
    "code_changes": "자동 변경된 코드 이력",
    "model_versions": "ML 모델 버전별 성과 이력",
}


class BotMemory:
    """PostgreSQL 기반 봇 장기 기억 저장소."""

    async def save(self, memory_type: str, content: dict) -> bool:
        """기억 저장."""
        if memory_type not in MEMORY_TYPES:
            logger.warning(f"알 수 없는 기억 유형: {memory_type}")
            return False
        # TODO: TimescaleDB/PostgreSQL 저장 구현
        logger.debug(f"기억 저장: [{memory_type}]")
        return True

    async def recall(self, memory_type: str, limit: int = 100) -> list[dict]:
        """기억 조회."""
        # TODO: DB 조회 구현
        return []

    async def get_failure_patterns(self, lookback_days: int = 90) -> list[dict]:
        """최근 N일 실패 패턴 조회."""
        # TODO: 손실 매매 패턴 집계 쿼리
        return []

    async def get_performance_summary(self) -> dict:
        """성과 요약 통계."""
        # TODO: 전략별/기간별 성과 집계
        return {
            "total_trades": 0,
            "win_rate": 0.0,
            "avg_return": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
        }
