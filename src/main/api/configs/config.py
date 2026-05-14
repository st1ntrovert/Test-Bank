from pathlib import Path
from typing import Any
import re
import os


class Config:
    _isinstance = None
    _dictionary = {}

    def __new__(cls):
        if cls._isinstance is None:
            cls._isinstance = super(Config, cls).__new__(cls)

            config_path = Path(__file__).parents[4] / 'resources' / 'urls.properties'

            if not config_path.exists():
                raise FileNotFoundError(f"Config path not found: {config_path}")

            with open(config_path, "r") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.split("=", 1)
                        cls._dictionary[key] = value.strip()

        cls._apply_env_overrides()

        return cls._isinstance

    @classmethod
    def _apply_env_overrides(cls) -> None:
        for key in cls._dictionary:
            env_key = cls._camel_to_upper_snake(key)
            env_value = os.environ.get(env_key)
            if env_value:
                cls._dictionary[key] = env_value

    @staticmethod
    def _camel_to_upper_snake(name: str) -> str:
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).upper()

    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        return Config()._dictionary.get(key, default_value)
