"""사용자 피드백 처리 + 반영."""

from loguru import logger
from self_learning.bot_memory import BotMemory


class FeedbackProcessor:
    """텔레그램으로 받은 사용자 피드백을 처리하고 시스템에 반영."""

    def __init__(self):
        self.memory = BotMemory()

    async def process(self, feedback_text: str, user_id: str):
        """피드백 텍스트 처리."""
        await self.memory.save("user_feedback", {
            "text": feedback_text,
            "user_id": user_id,
        })
        logger.info(f"피드백 저장: {feedback_text[:50]}...")
        # TODO: 피드백 내용에 따른 즉시 반영 로직
