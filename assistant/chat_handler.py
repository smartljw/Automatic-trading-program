"""메신저형 채팅 인터페이스 — 텔레그램 ↔ Claude Agent 연결."""

from loguru import logger
from assistant.claude_agent import ClaudeAgent
from assistant.command_parser import CommandParser


class ChatHandler:
    """텔레그램 메시지를 받아 적절한 에이전트로 라우팅."""

    def __init__(self):
        self.agent = ClaudeAgent()
        self.parser = CommandParser()

    async def handle(self, text: str, user_id: str) -> str:
        """메시지 처리 및 응답 반환."""
        # 1. 단순 명령 패턴 먼저 처리 (빠른 응답)
        parsed = self.parser.parse(text)
        if parsed:
            return await self._execute_command(parsed)

        # 2. Claude API로 자연어 처리
        return await self.agent.chat(text)

    async def _execute_command(self, cmd) -> str:
        """파싱된 명령 실행."""
        if cmd.action == "status":
            return "포트폴리오 현황: 조회 중..."
        elif cmd.action == "pause":
            return "⏸ 전략 일시 정지됨"
        elif cmd.action == "resume":
            return "▶️ 전략 재개됨"
        elif cmd.action == "emergency":
            return "🚨 긴급 청산 실행 중..."
        elif cmd.action in ("buy", "sell"):
            return f"{cmd.params.get('action', '주문')} 처리 중: {cmd.params}"
        return await self.agent.chat(f"명령 처리: {cmd.action}")
