"""일별/주별 자동 리포트 생성 및 전송."""

from datetime import datetime
from loguru import logger


class Reporter:
    """매일 오후 6시 자동으로 성과 리포트를 생성해 텔레그램으로 전송."""

    async def send_daily_report(self):
        """일별 리포트 생성 및 전송."""
        report = await self._build_daily_report()
        await self._send_telegram(report)

    async def _build_daily_report(self) -> str:
        today = datetime.now().strftime("%Y-%m-%d")
        # TODO: DB에서 오늘 매매 이력 및 성과 조회
        return f"""📅 {today} 일별 리포트
총 매매: 0건
실현 손익: 0원 (0.00%)
보유 종목: 0개
미실현 손익: 0원
내일 예정: 전략 0개 활성"""

    async def _send_telegram(self, text: str):
        """텔레그램 전송."""
        from assistant.telegram_bot import TelegramBot
        # TODO: 텔레그램 봇 인스턴스 공유 구조로 개선
        logger.info("리포트 텔레그램 전송")
