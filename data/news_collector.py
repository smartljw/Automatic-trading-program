"""네이버 뉴스 API + DART 공시 RSS 수집."""

import aiohttp
from datetime import datetime
from loguru import logger
from config.settings import settings


class NewsCollector:
    """네이버 뉴스 API로 종목 관련 뉴스를 수집."""

    NAVER_API_URL = "https://openapi.naver.com/v1/search/news.json"

    async def collect(self, stock_name: str, display: int = 20) -> list[dict]:
        """종목명으로 최신 뉴스 수집."""
        headers = {
            "X-Naver-Client-Id": settings.naver_client_id,
            "X-Naver-Client-Secret": settings.naver_client_secret,
        }
        params = {"query": stock_name, "display": display, "sort": "date"}

        async with aiohttp.ClientSession() as session:
            async with session.get(self.NAVER_API_URL, headers=headers, params=params) as resp:
                if resp.status != 200:
                    logger.error(f"네이버 뉴스 API 오류: {resp.status}")
                    return []
                data = await resp.json()
                return data.get("items", [])


class DARTCollector:
    """DART OpenAPI 공시 수집."""

    DART_RSS_URL = "https://dart.fss.or.kr/api/todayDart.xml"

    async def collect_rss(self) -> list[dict]:
        """DART 오늘의 공시 RSS 수집."""
        # TODO: DART RSS 파싱 구현
        return []

    async def collect_financials(self, stock_code: str, year: int, quarter: int) -> dict:
        """재무제표 수집 (분기별 실적)."""
        # TODO: DART OpenAPI 재무제표 조회 구현
        return {}
