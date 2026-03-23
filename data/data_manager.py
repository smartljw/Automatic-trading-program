"""데이터 통합 관리 — 수집/저장/조회 통합 인터페이스."""

from loguru import logger
from config.settings import DATA_UPDATE_SCHEDULE


class DataManager:
    """모든 데이터 수집기를 통합 관리하는 파사드."""

    def __init__(self):
        self._collectors = {}

    async def initialize(self):
        """수집기 초기화."""
        from data.chart_collector import ChartCollector
        from data.news_collector import NewsCollector, DARTCollector
        from data.macro_collector import MacroCollector
        from data.kis_stream import KISStream

        self._collectors = {
            "chart": ChartCollector(),
            "news": NewsCollector(),
            "dart": DARTCollector(),
            "macro": MacroCollector(),
            "stream": KISStream(),
        }
        logger.info("DataManager 초기화 완료")

    async def run_scheduled(self, schedule_key: str):
        """스케줄에 따른 데이터 수집 실행."""
        targets = DATA_UPDATE_SCHEDULE.get(schedule_key, [])
        for target in targets:
            logger.info(f"데이터 수집 실행: {target}")
            await self._collect(target)

    async def _collect(self, data_type: str):
        """개별 데이터 타입 수집."""
        # TODO: 각 타입별 수집 로직 구현
        pass
