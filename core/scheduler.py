"""작업 스케줄러 — 장 시작/종료 및 정기 작업 관리."""

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
from config.settings import settings, DATA_UPDATE_SCHEDULE

KST = pytz.timezone(settings.timezone)


class TradingScheduler:
    """APScheduler 기반 트레이딩 작업 스케줄러."""

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=KST)

    def setup_jobs(self):
        """모든 정기 작업 등록."""
        # 장 시작 전 (오전 9시)
        self.scheduler.add_job(
            self._pre_market, CronTrigger(hour=8, minute=50, timezone=KST),
            id="pre_market", replace_existing=True,
        )
        # 장 종료 후 (오후 3시 30분)
        self.scheduler.add_job(
            self._post_market, CronTrigger(hour=15, minute=35, timezone=KST),
            id="post_market", replace_existing=True,
        )
        # 30분마다 뉴스 수집
        self.scheduler.add_job(
            self._collect_news, "interval", minutes=30,
            id="news_collect", replace_existing=True,
        )
        # 야간 ML 재학습 (오전 2시)
        self.scheduler.add_job(
            self._nightly_retrain, CronTrigger(hour=2, minute=0, timezone=KST),
            id="nightly_retrain", replace_existing=True,
        )
        # 일일 리포트 (오후 6시)
        self.scheduler.add_job(
            self._daily_report, CronTrigger(hour=18, minute=0, timezone=KST),
            id="daily_report", replace_existing=True,
        )
        logger.info("스케줄러 작업 등록 완료")

    def start(self):
        self.setup_jobs()
        self.scheduler.start()
        logger.info("스케줄러 시작")

    def stop(self):
        self.scheduler.shutdown()
        logger.info("스케줄러 정지")

    async def _pre_market(self):
        """장 시작 전 — 재무/지표 데이터 업데이트, 리스크 초기화."""
        logger.info("장 시작 전 준비 작업 시작")

    async def _post_market(self):
        """장 종료 후 — 차트/외국인 데이터 업데이트, 성과 집계."""
        logger.info("장 마감 후 정리 작업 시작")

    async def _collect_news(self):
        """30분 간격 뉴스 수집."""
        logger.debug("뉴스 수집 실행")

    async def _nightly_retrain(self):
        """야간 ML 모델 재학습."""
        logger.info("야간 ML 재학습 시작")

    async def _daily_report(self):
        """일별 리포트 텔레그램 전송."""
        logger.info("일별 리포트 생성 및 전송")
