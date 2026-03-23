"""전략 생성/저장/활성화 관리."""

import yaml
from pathlib import Path
from datetime import datetime
from loguru import logger
from strategy.strategy_base import StrategyConfig

STRATEGY_CONFIG_PATH = Path("config/strategy_config.yaml")


class StrategyStore:
    """전략을 YAML 파일로 관리하는 저장소."""

    def __init__(self):
        self._strategies: dict[str, StrategyConfig] = {}
        self._load()

    def _load(self):
        """config/strategy_config.yaml 에서 전략 로드."""
        if not STRATEGY_CONFIG_PATH.exists():
            return
        with open(STRATEGY_CONFIG_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for s in data.get("active_strategies", []):
            config = StrategyConfig(
                name=s["name"],
                description=s.get("description", ""),
                active=s.get("active", False),
                stocks=s.get("stocks", []),
                buy_conditions=s.get("buy_conditions", []),
                sell_conditions=s.get("sell_conditions", []),
                position_size=s.get("position_size", 0.10),
            )
            self._strategies[config.name] = config
        logger.info(f"전략 {len(self._strategies)}개 로드 완료")

    def get_active(self) -> list[StrategyConfig]:
        """활성화된 전략 목록 반환."""
        return [s for s in self._strategies.values() if s.active]

    def get_all(self) -> list[StrategyConfig]:
        return list(self._strategies.values())

    def activate(self, name: str) -> bool:
        if name not in self._strategies:
            return False
        self._strategies[name].active = True
        self._save()
        logger.info(f"전략 활성화: {name}")
        return True

    def deactivate(self, name: str) -> bool:
        if name not in self._strategies:
            return False
        self._strategies[name].active = False
        self._save()
        logger.info(f"전략 비활성화: {name}")
        return True

    def add(self, config: StrategyConfig) -> bool:
        """새 전략 추가 (백테스트 통과 후)."""
        self._strategies[config.name] = config
        self._save()
        logger.info(f"새 전략 등록: {config.name}")
        return True

    def _save(self):
        """YAML 파일에 저장."""
        data = {
            "active_strategies": [
                {
                    "name": s.name,
                    "description": s.description,
                    "active": s.active,
                    "stocks": s.stocks,
                    "buy_conditions": s.buy_conditions,
                    "sell_conditions": s.sell_conditions,
                    "position_size": s.position_size,
                }
                for s in self._strategies.values()
            ]
        }
        with open(STRATEGY_CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
