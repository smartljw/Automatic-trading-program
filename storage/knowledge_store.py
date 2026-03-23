"""AI 학습 데이터 저장 — Parquet 포맷."""

import pandas as pd
from pathlib import Path
from loguru import logger
from config.settings import settings


class KnowledgeStore:
    """학습 데이터를 Parquet 포맷으로 저장/로드."""

    BASE_PATH = Path(settings.data_path)

    def save_ohlcv(self, stock_code: str, df: pd.DataFrame):
        """주가 데이터 Parquet 저장."""
        path = self.BASE_PATH / "ohlcv" / f"{stock_code}.parquet"
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, compression="snappy")
        logger.debug(f"OHLCV 저장: {path}")

    def load_ohlcv(self, stock_code: str) -> pd.DataFrame:
        """주가 데이터 Parquet 로드."""
        path = self.BASE_PATH / "ohlcv" / f"{stock_code}.parquet"
        if not path.exists():
            return pd.DataFrame()
        return pd.read_parquet(path)

    def save_features(self, stock_code: str, df: pd.DataFrame):
        """ML 특징 데이터 저장."""
        path = self.BASE_PATH / "features" / f"{stock_code}.parquet"
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, compression="snappy")
