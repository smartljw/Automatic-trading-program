"""
KIS API 주문 실행기.
CLAUDE.md 규칙: 변경 시 반드시 모의투자 테스트 먼저 실행.
"""

import aiohttp
from loguru import logger
from config.settings import settings
from config.risk_limits import HARD_LIMITS


class OrderExecutor:
    """KIS REST API를 통해 실제 주문을 실행."""

    def __init__(self):
        self.paper_trade = settings.kis_paper_trade
        self.base_url = settings.kis_base_url
        self._access_token: str = ""

        if self.paper_trade:
            logger.warning("⚠️  모의투자 모드로 실행 중 — 실제 주문 없음")
        else:
            logger.warning("🚨 실전투자 모드 — 실제 자금 사용!")

    async def authenticate(self) -> bool:
        """KIS API 접근 토큰 발급."""
        url = f"{self.base_url}/oauth2/tokenP"
        payload = {
            "grant_type": "client_credentials",
            "appkey": settings.kis_app_key,
            "appsecret": settings.kis_app_secret,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self._access_token = data.get("access_token", "")
                    logger.info("KIS API 인증 성공")
                    return True
                logger.error(f"KIS API 인증 실패: {resp.status}")
                return False

    async def buy(self, stock_code: str, quantity: int, price: int = 0) -> dict:
        """매수 주문. price=0 이면 시장가."""
        logger.info(f"매수 주문: {stock_code} {quantity}주 {'시장가' if price == 0 else f'{price:,}원'}")
        # TODO: KIS API 매수 엔드포인트 구현
        return {"status": "pending", "stock_code": stock_code, "quantity": quantity}

    async def sell(self, stock_code: str, quantity: int, price: int = 0) -> dict:
        """매도 주문. price=0 이면 시장가."""
        logger.info(f"매도 주문: {stock_code} {quantity}주 {'시장가' if price == 0 else f'{price:,}원'}")
        # TODO: KIS API 매도 엔드포인트 구현
        return {"status": "pending", "stock_code": stock_code, "quantity": quantity}

    async def cancel(self, order_no: str) -> bool:
        """주문 취소."""
        logger.info(f"주문 취소: {order_no}")
        # TODO: KIS API 취소 엔드포인트 구현
        return True

    async def get_balance(self) -> dict:
        """계좌 잔고 조회."""
        # TODO: KIS API 잔고 조회 구현
        return {"total_value": 0, "cash": 0, "stocks": []}

    async def emergency_sell_all(self) -> bool:
        """전체 포지션 긴급 청산 (/emergency 명령)."""
        logger.critical("🚨 긴급 전체 청산 실행!")
        # TODO: 보유 종목 전량 시장가 매도
        return True
