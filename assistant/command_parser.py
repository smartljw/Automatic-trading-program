"""자연어 명령 → 시스템 명령 변환."""

import re
from dataclasses import dataclass
from loguru import logger


@dataclass
class ParsedCommand:
    action: str         # buy | sell | pause | resume | status | ...
    params: dict


class CommandParser:
    """자연어 텍스트에서 매매/시스템 명령을 추출."""

    # 단순 패턴 매칭 (Claude API 보조 전 빠른 처리)
    PATTERNS = [
        (r"(.+?)\s*(\d+)\s*주\s*매수", "buy"),
        (r"(.+?)\s*(\d+)\s*주\s*매도", "sell"),
        (r"전체\s*청산|긴급\s*청산", "emergency"),
        (r"정지|일시정지|멈춰", "pause"),
        (r"재개|다시\s*시작", "resume"),
        (r"현황|상태|포트폴리오", "status"),
        (r"리포트|보고서", "report"),
    ]

    def parse(self, text: str) -> ParsedCommand | None:
        """텍스트에서 명령 추출. 매칭 없으면 None 반환."""
        for pattern, action in self.PATTERNS:
            match = re.search(pattern, text)
            if match:
                params = {}
                if action in ("buy", "sell") and match.lastindex >= 2:
                    params["stock_name"] = match.group(1).strip()
                    params["quantity"] = int(match.group(2))
                return ParsedCommand(action=action, params=params)
        return None
