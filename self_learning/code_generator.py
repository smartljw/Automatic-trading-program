"""새 모듈/에이전트 자동 생성 (레벨 D 자가학습)."""

import anthropic
from loguru import logger
from config.settings import settings


class CodeGenerator:
    """Claude API로 새 기능 코드를 자동 생성하고 테스트를 통과하면 시스템에 통합."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    async def generate_module(self, requirement: str, module_type: str) -> str:
        """요구사항에 맞는 새 모듈 코드 생성."""
        system_prompt = f"""
너는 Python 트레이딩 봇 개발자야.
요구사항에 맞는 깔끔한 Python 모듈 코드만 반환해.
모듈 타입: {module_type} (collector | strategy | analyzer)
코딩 규칙:
- API 키는 반드시 config.settings 에서 로드
- 모든 외부 호출은 async/await 사용
- 에러는 loguru logger로 처리
"""
        response = self.client.messages.create(
            model=settings.claude_model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": requirement}],
        )
        code = response.content[0].text
        logger.info(f"새 모듈 코드 생성: {module_type}")
        return code

    async def validate_and_integrate(self, code: str, module_name: str) -> bool:
        """생성된 코드 테스트 실행 후 통과 시 시스템에 통합."""
        # TODO: 샌드박스 환경에서 코드 실행 테스트
        # TODO: 테스트 통과 시 파일로 저장 + orchestrator에 등록
        logger.info(f"코드 검증 중: {module_name}")
        return False  # Phase 4에서 구현
