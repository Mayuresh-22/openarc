import os
import json
from os.path import dirname as up

from src.types.config import ConfigFileType
from src.utils.file import ensure_file_exists


ROOT_PATH = up(up(up(__file__)))
CONFIG_PATH = os.path.join(ROOT_PATH, ".openarc/config.json")

# Ensure config file exists at startup
ensure_file_exists(
    CONFIG_PATH, default_content=ConfigFileType().model_dump_json(indent=4)
)


class ConfigService:
    _instance = None

    def __new__(cls) -> "ConfigService":
        if cls._instance is None:
            cls._instance = super(ConfigService, cls).__new__(cls)
        return cls._instance

    def load_config(self) -> ConfigFileType:
        with open(CONFIG_PATH, "r") as f:
            self.config_file = ConfigFileType(**json.load(f))
        return self.config_file

    def save_config(self):
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config_file.model_dump(), f, indent=4)

    def update_config(self, new_config: dict):
        self.config_file = self.load_config()
        for key, value in new_config.items():
            setattr(self.config_file, key, value)
        self.save_config()
