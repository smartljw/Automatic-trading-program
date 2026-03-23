#!/bin/bash
# 트레이딩 봇 전체 시작 스크립트

set -e

echo "=== Trading AI Bot 시작 ==="

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "오류: .env 파일이 없습니다. .env.example 을 복사해서 .env 를 만드세요."
    exit 1
fi

# Docker Compose로 DB 먼저 시작
echo "[1/3] 데이터베이스 시작 중..."
docker compose up -d timescaledb redis
sleep 5

# DB 마이그레이션
echo "[2/3] DB 마이그레이션..."
docker compose exec timescaledb psql -U trading_user -d trading -f /docker-entrypoint-initdb.d/001_init.sql 2>/dev/null || true

# 봇 시작
echo "[3/3] 트레이딩 봇 시작..."
docker compose up -d bot dashboard

echo "=== 시작 완료 ==="
echo "대시보드: http://localhost:8000"
echo "로그 확인: docker compose logs -f bot"
