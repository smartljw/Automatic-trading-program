#!/bin/bash
# 수동 ML 모델 재학습 실행

echo "=== ML 모델 재학습 시작 ==="
docker compose --profile training up trainer
echo "=== 재학습 완료 ==="
