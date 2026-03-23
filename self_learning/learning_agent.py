"""Claude API 기반 자기개선 엔진."""

import json
import anthropic
from loguru import logger
from config.settings import settings

SELF_LEARNING_SYSTEM_PROMPT = """
너는 trading-ai-bot의 자기개선 엔진이야.
주어진 성과 데이터와 실패 패턴을 분석해서
구체적인 개선안을 JSON으로만 응답해.

응답 형식:
{
  "analysis": "현재 문제점 분석",
  "change_type": "PARAM | RULE | RETRAIN | NEW_MODULE",
  "changes": [...],
  "expected_impact": "예상 효과",
  "risk_level": "LOW | MEDIUM | HIGH",
  "requires_approval": true/false
}

절대 불변 규칙:
- 종목당 최대 비중 25% 초과 불가
- 일일 손실 한도 5% 초과 완화 불가
- 드로우다운 10% 초과 시 전략 정지는 제거 불가
"""


class LearningAgent:
    """Claude API를 사용해 성과 분석 및 자동 개선안을 도출."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def analyze_and_improve(self, performance_data: dict, failure_patterns: list) -> dict:
        """성과 데이터 + 실패 패턴 분석 → 개선안 생성."""
        user_message = f"""
최근 성과 데이터:
{json.dumps(performance_data, ensure_ascii=False, indent=2)}

실패 패턴:
{json.dumps(failure_patterns, ensure_ascii=False, indent=2)}

위 데이터를 분석해서 구체적인 개선안을 JSON으로 제시해줘.
"""
        try:
            response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=2048,
                system=SELF_LEARNING_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            result = json.loads(response.content[0].text)
            logger.info(f"자기개선 분석 완료: change_type={result.get('change_type')}, risk={result.get('risk_level')}")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"개선안 JSON 파싱 실패: {e}")
            return {}
        except Exception as e:
            logger.error(f"LearningAgent 오류: {e}")
            return {}

    async def apply_safe_changes(self, improvement: dict) -> bool:
        """승인 불필요한 안전 변경만 자동 적용."""
        if improvement.get("requires_approval"):
            logger.info("사용자 승인 필요 — 텔레그램으로 요청 전송")
            return False

        if improvement.get("risk_level") == "HIGH":
            logger.warning("HIGH 리스크 변경 — 자동 적용 건너뜀")
            return False

        # TODO: PARAM 변경 자동 적용 로직
        logger.info(f"안전 변경 적용: {improvement.get('changes')}")
        return True
