"""학습된 지식 + 인사이트 데이터베이스."""

from loguru import logger


class KnowledgeBase:
    """시장 인사이트와 학습 결과를 축적하는 지식 저장소."""

    async def store_insight(self, category: str, insight: str, confidence: float):
        """새 인사이트 저장."""
        # TODO: PostgreSQL 저장
        logger.debug(f"인사이트 저장 [{category}]: {insight[:50]}...")

    async def query(self, query: str, top_k: int = 5) -> list[dict]:
        """관련 인사이트 검색."""
        # TODO: 벡터 유사도 검색 또는 키워드 검색
        return []

    async def get_market_regime_insights(self, regime: str) -> list[dict]:
        """특정 시장 국면(상승/하락/횡보)에서의 전략 성과 인사이트."""
        return await self.query(f"market_regime:{regime}")
