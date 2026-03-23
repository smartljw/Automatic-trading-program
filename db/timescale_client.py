"""TimescaleDB 연결 및 시계열 데이터 관리."""

import asyncpg
from loguru import logger
from config.settings import settings


class TimescaleClient:
    """asyncpg 기반 TimescaleDB 클라이언트."""

    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def connect(self):
        """연결 풀 생성."""
        self._pool = await asyncpg.create_pool(
            settings.timescale_url,
            min_size=2,
            max_size=10,
        )
        logger.info("TimescaleDB 연결 완료")

    async def disconnect(self):
        if self._pool:
            await self._pool.close()

    async def execute(self, query: str, *args):
        async with self._pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args) -> list:
        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def insert_price(self, stock_code: str, timestamp, open_: float, high: float, low: float, close: float, volume: int):
        """주가 데이터 삽입."""
        await self.execute(
            """
            INSERT INTO prices (time, stock_code, open, high, low, close, volume)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (time, stock_code) DO NOTHING
            """,
            timestamp, stock_code, open_, high, low, close, volume,
        )

    async def get_ohlcv(self, stock_code: str, start, end) -> list:
        """주가 데이터 조회."""
        return await self.fetch(
            "SELECT * FROM prices WHERE stock_code=$1 AND time BETWEEN $2 AND $3 ORDER BY time",
            stock_code, start, end,
        )
