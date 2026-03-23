# ============================================================
# trading-ai-bot Dockerfile (멀티 스테이지)
# ============================================================

FROM python:3.11-slim AS base

WORKDIR /app

# 시스템 의존성
RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ─── 대시보드 타겟 ───
FROM base AS dashboard
EXPOSE 8000
CMD ["uvicorn", "monitoring.dashboard_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ─── 봇 코어 타겟 ───
FROM base AS bot
CMD ["python", "-m", "core.orchestrator"]

# ─── ML 트레이너 타겟 ───
FROM base AS trainer
CMD ["python", "-c", "import asyncio; from ai.model_trainer import ModelTrainer; asyncio.run(ModelTrainer().run_nightly())"]
