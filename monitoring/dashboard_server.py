"""FastAPI 웹 대시보드 서버."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from config.settings import settings

app = FastAPI(title="Trading AI Bot Dashboard", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/portfolio")
async def get_portfolio():
    """계좌 현황 조회."""
    # TODO: OrderExecutor.get_balance() 연동
    return {"total_value": 0, "cash": 0, "daily_pnl": 0, "stocks": []}


@app.get("/api/strategies")
async def get_strategies():
    """활성 전략 목록 조회."""
    from strategy.strategy_store import StrategyStore
    store = StrategyStore()
    return {"strategies": [{"name": s.name, "active": s.active} for s in store.get_all()]}


@app.get("/api/trades")
async def get_trades(limit: int = 50):
    """최근 매매 이력 조회."""
    # TODO: DB 연동
    return {"trades": []}


@app.get("/api/ai-status")
async def get_ai_status():
    """AI 봇 상태 조회."""
    return {
        "bot_status": "running",
        "last_retrain": None,
        "next_retrain": None,
        "model_versions": {},
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.dashboard_port)
