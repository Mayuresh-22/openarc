import os
import json
from os.path import dirname as up

from src.types.config import ConfigFileType


ROOT_PATH = up(up(up(__file__)))
CONFIG_PATH = os.path.join(up(up(up(__file__))), ".openarc/config.json")

if not os.path.exists(CONFIG_PATH):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        f.write("{}")


class ConfigService:
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
