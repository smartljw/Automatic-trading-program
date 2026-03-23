"""FinBERT 기반 뉴스 감성 분석."""

from loguru import logger


class SentimentAnalyzer:
    """FinBERT 모델로 뉴스 기사의 감성(긍정/부정/중립)을 분석."""

    MODEL_NAME = "snunlp/KR-FinBert-SC"  # 한국어 금융 FinBERT

    def __init__(self):
        self.pipeline = None
        self._loaded = False

    def load(self):
        """FinBERT 모델 로드 (최초 실행 시 다운로드)."""
        try:
            from transformers import pipeline
            self.pipeline = pipeline(
                "text-classification",
                model=self.MODEL_NAME,
                device=-1,  # CPU; GPU 사용 시 device=0
            )
            self._loaded = True
            logger.info(f"FinBERT 로드 완료: {self.MODEL_NAME}")
        except Exception as e:
            logger.error(f"FinBERT 로드 실패: {e}")

    def analyze(self, texts: list[str]) -> dict:
        """텍스트 목록의 감성 분석. 반환: {'positive': 0~1, 'negative': 0~1, 'neutral': 0~1}"""
        if not self._loaded or not texts:
            return {"positive": 0.0, "negative": 0.0, "neutral": 1.0}

        results = self.pipeline(texts, truncation=True, max_length=512)
        scores = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}

        for r in results:
            label = r["label"].lower()
            if label in scores:
                scores[label] += r["score"] / len(results)

        return scores

    def to_signal_confidence(self, sentiment: dict) -> tuple[str, float]:
        """감성 점수를 매매 신호로 변환."""
        if sentiment["positive"] > 0.6:
            return "BUY", sentiment["positive"]
        elif sentiment["negative"] > 0.6:
            return "SELL", sentiment["negative"]
        return "HOLD", sentiment["neutral"]
