"""KIS WebSocket 실시간 시세 스트림."""

import asyncio
import json
import websockets
from loguru import logger
from config.settings import settings


class KISStream:
    """KIS WebSocket으로 실시간 체결가/호가/거래량 수신."""

    def __init__(self):
        self.ws_url = settings.kis_ws_url
        self._subscriptions: set[str] = set()
        self._callbacks: dict = {}

    async def connect(self):
        """WebSocket 연결."""
        logger.info(f"KIS WebSocket 연결: {self.ws_url}")
        async with websockets.connect(self.ws_url) as ws:
            await self._on_connected(ws)

    async def subscribe(self, stock_code: str, callback):
        """종목 실시간 시세 구독."""
        self._subscriptions.add(stock_code)
        self._callbacks[stock_code] = callback
        logger.debug(f"구독 추가: {stock_code}")

    async def unsubscribe(self, stock_code: str):
        """구독 해제."""
        self._subscriptions.discard(stock_code)
        self._callbacks.pop(stock_code, None)

    async def _on_connected(self, ws):
        """연결 후 구독 요청 전송."""
        # TODO: KIS WebSocket 구독 프로토콜 구현
        pass

    async def _handle_message(self, message: str):
        """수신 메시지 파싱 및 콜백 호출."""
        # TODO: KIS 실시간 데이터 파싱
        pass
