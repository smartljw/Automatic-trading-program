#!/bin/bash
# 트레이딩 봇 정지

echo "=== Trading AI Bot 정지 ==="
docker compose stop bot dashboard
echo "봇 정지 완료. DB는 유지됩니다."
echo "전체 정지: docker compose down"
