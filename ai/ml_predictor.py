"""LSTM + XGBoost 가격 방향 예측 모델."""

import numpy as np
import pandas as pd
from pathlib import Path
from loguru import logger
from config.settings import settings


class MLPredictor:
    """LSTM(PyTorch) + XGBoost 앙상블 예측기."""

    MODEL_PATH = Path(settings.model_path)

    def __init__(self):
        self.lstm_model = None
        self.xgb_model = None
        self._loaded = False

    def load(self):
        """저장된 모델 로드."""
        try:
            self._load_lstm()
            self._load_xgb()
            self._loaded = True
            logger.info("ML 모델 로드 완료")
        except FileNotFoundError:
            logger.warning("저장된 ML 모델 없음 — 학습 필요")

    def predict(self, features: pd.DataFrame) -> tuple[float, float]:
        """다음 봉 방향 예측. 반환: (방향_확률, 신뢰도)"""
        if not self._loaded:
            return 0.5, 0.0

        lstm_prob = self._predict_lstm(features)
        xgb_prob = self._predict_xgb(features)

        ensemble_prob = (lstm_prob + xgb_prob) / 2
        confidence = abs(ensemble_prob - 0.5) * 2

        return ensemble_prob, confidence

    def _load_lstm(self):
        lstm_path = self.MODEL_PATH / "lstm_model.pt"
        if lstm_path.exists():
            import torch
            # TODO: LSTM 모델 정의 및 로드
            pass

    def _load_xgb(self):
        xgb_path = self.MODEL_PATH / "xgb_model.json"
        if xgb_path.exists():
            import xgboost as xgb
            self.xgb_model = xgb.XGBClassifier()
            self.xgb_model.load_model(xgb_path)

    def _predict_lstm(self, features: pd.DataFrame) -> float:
        # TODO: LSTM 추론
        return 0.5

    def _predict_xgb(self, features: pd.DataFrame) -> float:
        if self.xgb_model is None:
            return 0.5
        # TODO: XGBoost 추론
        return 0.5
