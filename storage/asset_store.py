"""차트 이미지 등 파일 저장."""

from pathlib import Path
from loguru import logger
from config.settings import settings


class AssetStore:
    """백테스트 차트, 스크린샷 등 파일 관리."""

    BASE_PATH = Path(settings.data_path) / "assets"

    def __init__(self):
        self.BASE_PATH.mkdir(parents=True, exist_ok=True)

    def save_chart(self, name: str, image_bytes: bytes) -> Path:
        path = self.BASE_PATH / "charts" / f"{name}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(image_bytes)
        logger.debug(f"차트 저장: {path}")
        return path

    def get_chart(self, name: str) -> bytes | None:
        path = self.BASE_PATH / "charts" / f"{name}.png"
        if path.exists():
            return path.read_bytes()
        return None
