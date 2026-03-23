"""전체 모듈 조율 — 메인 루프."""

import asyncio
from loguru import logger
from config.settings import settings
from config.risk_limits import HARD_LIMITS


class Orchestrator:
    """트레이딩 봇 전체 모듈을 조율하는 중앙 컨트롤러."""

    def __init__(self):
        self.running = False
        self.paused = False

    async def start(self):
        """봇 시작."""
        logger.info("Orchestrator 시작")
        self.running = True
        await self._main_loop()

    async def stop(self):
        """봇 정지."""
        logger.info("Orchestrator 정지")
        self.running = False

    def pause(self):
        """전략 일시 정지."""
        self.paused = True
        logger.warning("전략 일시 정지됨")

    def resume(self):
        """전략 재개."""
        self.paused = False
        logger.info("전략 재개됨")

    async def _main_loop(self):
        """메인 루프 — 매 틱마다 신호 수집 및 주문 처리."""
        while self.running:
            try:
                if not self.paused:
                    await self._process_tick()
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"메인 루프 오류: {e}")
                await asyncio.sleep(5)

    async def _process_tick(self):
        """단일 틱 처리 — 신호 수집 → 리스크 검사 → 주문 실행."""
        # TODO: Phase 1 구현
        pass


if __name__ == "__main__":
    orchestrator = Orchestrator()
    asyncio.run(orchestrator.start())
