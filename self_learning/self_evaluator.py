"""스스로 성과 평가 + 개선안 도출."""

from loguru import logger
from self_learning.bot_memory import BotMemory
from self_learning.learning_agent import LearningAgent


class SelfEvaluator:
    """주기적으로 자신의 성과를 평가하고 개선 사이클을 실행."""

    def __init__(self):
        self.memory = BotMemory()
        self.agent = LearningAgent()

    async def run_evaluation_cycle(self):
        """평가 → 분석 → 개선안 도출 → 적용 사이클."""
        logger.info("자기 평가 사이클 시작")

        performance = await self.memory.get_performance_summary()
        failure_patterns = await self.memory.get_failure_patterns(lookback_days=30)

        improvement = await self.agent.analyze_and_improve(performance, failure_patterns)

        if improvement:
            applied = await self.agent.apply_safe_changes(improvement)
            if applied:
                await self.memory.save("code_changes", {
                    "change": improvement,
                    "applied": True,
                })
            else:
                # 승인 필요 항목은 텔레그램으로 전송
                logger.info("사용자 승인 대기 중인 개선안 있음")

        logger.info("자기 평가 사이클 완료")
