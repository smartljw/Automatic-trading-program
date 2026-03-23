"""야간 자동 ML 모델 재학습."""

from loguru import logger
from pathlib import Path
from config.settings import settings


class ModelTrainer:
    """최신 데이터로 LSTM + XGBoost를 야간에 재학습."""

    MODEL_PATH = Path(settings.model_path)

    async def run_nightly(self):
        """야간 배치 재학습 실행."""
        logger.info("야간 ML 재학습 시작")
        try:
            await self._retrain_xgboost()
            await self._retrain_lstm()
            logger.info("야간 ML 재학습 완료")
        except Exception as e:
            logger.error(f"재학습 실패: {e}")
            raise

    async def _retrain_xgboost(self):
        """XGBoost 모델 재학습."""
        logger.info("XGBoost 재학습 중...")
        # TODO: DB에서 최신 데이터 로드 → 학습 → 성과 비교 → 교체

    async def _retrain_lstm(self):
        """LSTM 모델 재학습."""
        logger.info("LSTM 재학습 중...")
        # TODO: 시계열 데이터 로드 → PyTorch 학습 → 성과 비교 → 교체

    def _should_replace(self, new_accuracy: float, old_accuracy: float) -> bool:
        """성과가 향상된 경우에만 모델 교체."""
        return new_accuracy >= old_accuracy
