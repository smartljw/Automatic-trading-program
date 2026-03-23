"""텔레그램 봇 — 핸드폰 조작 인터페이스."""

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from loguru import logger
from config.settings import settings


class TelegramBot:
    """telegram.ext 기반 텔레그램 봇."""

    def __init__(self):
        self.app = Application.builder().token(settings.telegram_bot_token).build()
        self._register_handlers()

    def _register_handlers(self):
        """명령어 핸들러 등록."""
        commands = {
            "status": self.cmd_status,
            "positions": self.cmd_positions,
            "pause": self.cmd_pause,
            "resume": self.cmd_resume,
            "emergency": self.cmd_emergency,
            "report": self.cmd_report,
            "watchlist": self.cmd_watchlist,
            "strategies": self.cmd_strategies,
        }
        for cmd, handler in commands.items():
            self.app.add_handler(CommandHandler(cmd, handler))

        # 자연어 메시지 처리
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self):
        await self.app.run_polling()

    async def send_message(self, text: str):
        """메시지 전송 유틸리티."""
        await self.app.bot.send_message(chat_id=settings.telegram_chat_id, text=text)

    # ─── 명령어 핸들러 ───

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """포트폴리오 현황 + 오늘 수익률."""
        await update.message.reply_text("포트폴리오 현황 조회 중...")
        # TODO: 계좌 조회 후 응답

    async def cmd_positions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """보유 종목 목록."""
        await update.message.reply_text("보유 종목 조회 중...")

    async def cmd_pause(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """전략 일시 정지."""
        await update.message.reply_text("⏸ 전략이 일시 정지됩니다.")

    async def cmd_resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """전략 재개."""
        await update.message.reply_text("▶️ 전략이 재개됩니다.")

    async def cmd_emergency(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """긴급 전체 청산."""
        await update.message.reply_text("🚨 긴급 청산을 실행합니다...")
        # TODO: OrderExecutor.emergency_sell_all() 호출

    async def cmd_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """오늘 매매 요약 리포트."""
        await update.message.reply_text("📊 오늘 리포트 생성 중...")

    async def cmd_watchlist(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """관심 종목 목록."""
        await update.message.reply_text("관심 종목 목록 조회 중...")

    async def cmd_strategies(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """활성 전략 목록."""
        await update.message.reply_text("활성 전략 목록 조회 중...")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """자연어 메시지 → Claude API로 처리."""
        from assistant.claude_agent import ClaudeAgent
        agent = ClaudeAgent()
        response = await agent.chat(update.message.text)
        await update.message.reply_text(response)
