"""훈련된 모델 버전 관리."""

from pathlib import Path
from datetime import datetime
from loguru import logger
from config.settings import settings


class ModelStore:
    """모델 파일을 버전별로 저장하고 best 모델을 관리."""

    MODEL_PATH = Path(settings.model_path)

    def save(self, model_name: str, model, metrics: dict):
        """모델 저장 (버전 태깅)."""
        version = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.MODEL_PATH / model_name / version
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"모델 저장: {model_name} v{version} | metrics={metrics}")
        # TODO: 모델 직렬화 (torch.save / xgb.save_model)

    def load_best(self, model_name: str):
        """최고 성능 모델 로드."""
        best_path = self.MODEL_PATH / model_name / "best"
        if not best_path.exists():
            logger.warning(f"Best 모델 없음: {model_name}")
            return None
        # TODO: 모델 역직렬화
        return None

    def promote_to_best(self, model_name: str, version: str):
        """특정 버전을 best로 승격."""
        src = self.MODEL_PATH / model_name / version
        best = self.MODEL_PATH / model_name / "best"
        if best.exists():
            import shutil
            shutil.rmtree(best)
        import shutil
        shutil.copytree(src, best)
        logger.info(f"모델 승격: {model_name} v{version} → best")
