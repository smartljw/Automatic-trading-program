"""강화학습 에이전트 — PPO (stable-baselines3)."""

from loguru import logger
from pathlib import Path
from config.settings import settings


class RLAgent:
    """PPO 기반 강화학습 트레이딩 에이전트 (Phase 4)."""

    MODEL_PATH = Path(settings.model_path) / "rl_ppo_model"

    def __init__(self):
        self.model = None
        self._loaded = False

    def load(self):
        """저장된 PPO 모델 로드."""
        try:
            from stable_baselines3 import PPO
            if self.MODEL_PATH.exists():
                self.model = PPO.load(self.MODEL_PATH)
                self._loaded = True
                logger.info("PPO 모델 로드 완료")
        except Exception as e:
            logger.error(f"PPO 모델 로드 실패: {e}")

    def predict(self, observation) -> tuple[int, float]:
        """환경 관측값으로 행동 결정. 반환: (action, confidence)"""
        if not self._loaded:
            return 0, 0.0  # 관망
        action, _ = self.model.predict(observation, deterministic=True)
        return int(action), 0.7

    def train(self, env, total_timesteps: int = 100_000):
        """환경에서 PPO 학습."""
        from stable_baselines3 import PPO
        self.model = PPO("MlpPolicy", env, verbose=1)
        self.model.learn(total_timesteps=total_timesteps)
        self.model.save(self.MODEL_PATH)
        logger.info(f"PPO 학습 완료: {total_timesteps:,} 스텝")
