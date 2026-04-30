import json
from pathlib import Path

class ConfigLoader:
    _config = None

    @classmethod
    def load(cls):
        if cls._config is None:
            config_path = Path(__file__).parent.parent / "config.json"
            if not config_path.exists():
                raise FileNotFoundError(f"Config not found: {config_path}")

            with open(config_path, encoding="utf-8") as f:
                cls._config = json.load(f)

        return cls._config