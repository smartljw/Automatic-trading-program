"""Claude API 총괄 LLM — 자연어 명령 처리 및 AI 비서."""

import anthropic
from loguru import logger
from config.settings import settings

TRADING_ASSISTANT_PROMPT = """
너는 trading-ai-bot의 AI 비서야.
사용자의 자연어 메시지를 분석해서 적절한 시스템 명령을 실행하거나
시장 상황을 분석해서 친절하게 설명해줘.

가능한 명령:
- 주문 실행 (매수/매도/청산)
- 전략 관리 (활성화/비활성화/생성)
- 성과 분석 및 리포트
- 시장 분석
- 자기학습 트리거

응답은 항상 한국어로, 핵심만 간결하게 말해줘.
"""


class ClaudeAgent:
    """Claude API를 사용하는 메인 LLM 에이전트."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._conversation_history: list[dict] = []

    async def chat(self, user_message: str) -> str:
        """사용자 메시지 처리 및 응답 생성."""
        self._conversation_history.append({"role": "user", "content": user_message})

        try:
            response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=1024,
                system=TRADING_ASSISTANT_PROMPT,
                messages=self._conversation_history[-20:],  # 최근 20턴 컨텍스트
            )
            reply = response.content[0].text
            self._conversation_history.append({"role": "assistant", "content": reply})
            return reply

        except Exception as e:
            logger.error(f"Claude API 오류: {e}")
            return "죄송해요, 일시적인 오류가 발생했어요. 잠시 후 다시 시도해주세요."

    async def analyze_market(self, stock_code: str, data: dict) -> str:
        """특정 종목 시장 분석."""
        prompt = f"종목 {stock_code}의 현재 상황을 분석해줘:\n{data}"
        return await self.chat(prompt)

    def clear_history(self):
        """대화 히스토리 초기화."""
        self._conversation_history.clear()
